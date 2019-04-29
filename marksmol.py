import sys
import os
import pathlib


def parse(t,path,debug = False):
    os.chdir(path)
    #Current strings
    code = ''
    word = ''
    line = ''
    
    #State trackers
    inQuotes = 0
    inComment = 0 #not bool so it can have comments in comments
    escapeNext = False

    #Indentation/Parent tracking
    indentation = 0
    tagStack = []
    rootIndentation = -1

    #Functions/Templates stuff
    inFunc = False
    funcFirst = True
    textNext = False
    funcs = []

    t = t.replace(' '*4, '\t').replace("\r\n",'\n') #Replace 4 spaces with tabs, replace \r\n with \n

    class marksmolFunc:
        def __init__(self,name,variables,text):
            self.name = name
            self.variables = variables
            self.text = text

    #DEBUG
    def dprint(txt):
        nonlocal debug
        if debug:
            print(txt)

    #Get second to last tag (pop it)
    def getPrevTag():
        nonlocal tagStack

        tag = tagStack.pop()
        if len(tagStack) is not 0:
            retTag = tagStack.pop()
            tagStack.append(tag)
            return retTag
        return tag

    def clearFn():
            nonlocal funcs,inFunc,textNext,funcFirst
            funcs.pop()
            
            inFunc = False
            textNext = False
            funcFirst = True
            return

    def funcEnd(l):
        nonlocal code, word, tagStack, line, indentation, inFunc, funcFirst, funcs, textNext, t
        
        fnInd = -1

        if funcs[-1].name == '$include':
            textToPaste = pathlib.Path(funcs[-1].variables[0][1:]).read_text().replace('\r\n','\n')
            textToPaste = '\t'*indentation + textToPaste.replace('\n','\n'+'\t'*indentation) #indent
            t = t[:l+1] + '\n' + textToPaste + t[l+1:]
            
            clearFn()
        elif funcs[-1].name == '$includeText':
            textToPaste = pathlib.Path(funcs[-1].variables[0][1:]).read_text().replace('\r\n','\n')
            textToPaste = '\t'*indentation + '`' + textToPaste.replace('\n','\n'+'\t'*indentation) + '`' #indent
            t = t[:l+1] + '\n' + textToPaste + t[l+1:]
            
            clearFn()
        elif funcs[-1].name == '$strip':
            textToPaste = funcs[-1].variables[0].replace('\r\n','\n')
            textToPaste = textToPaste.rstrip('`').lstrip('`').rstrip('\`').lstrip('\`')
            textToPaste = '\t'*indentation + textToPaste.replace('\n','\n'+'\t'*indentation) #indent
            t = t[:l+1] + '\n' + textToPaste + t[l+1:]
            
            clearFn()
        elif funcs[-1].name == '$str':
            textToPaste = funcs[-1].variables[0].replace('\r\n','\n')
            textToPaste = textToPaste.rstrip('`').lstrip('`').rstrip('\`').lstrip('\`')
            textToPaste = '\t'*indentation + textToPaste.replace('\n','\n'+'\t'*indentation) #indent
            t = t[:l+1] + '\n' + '`' + textToPaste + '`' + t[l+1:]
            
            clearFn()
        else:

            for x in range(len(funcs)):
                #dprint('search ['+str(x)+'] name: |' + funcs[x].name + '| vs |' + funcs[-1].name + '|')
                if funcs[x].name == funcs[-1].name:
                    fnInd = x
                    break
                    

            dprint('fnInd : ' + str(fnInd))
            
            if fnInd is (len(funcs)-1) or fnInd is -1:
                #Is new
                dprint('fn is new')

                textNext = True
            else:
                #Do function stuff
                dprint('fn is old')
                
                textToPaste = funcs[fnInd].text.replace('\r\n','\n')

                textToPaste = '\t'*indentation + textToPaste.replace('\n','\n'+'\t'*indentation) #indent

                #dprint('FUNCTION TEXT:\n' + textToPaste)

                #replace var names with var values
                for i in range(len(funcs[-1].variables)):
                    #dprint(funcs[fnInd].variables[i] + ' replaced w: ' + funcs[-1].variables[i][1:])
                    textToPaste = textToPaste.replace(funcs[fnInd].variables[i],funcs[-1].variables[i][1:])

                t = t[:l+1] + '\n' + textToPaste + t[l+1:]
                
                #dprint('\n\n\nFUNCTION TEXT REPLACED:\n' + textToPaste + '\n\n')

                dprint('\n\nFUNCTION T RESULT:\n' + t + '\n\n')

                clearFn()

    def endWord():
        nonlocal code, word, tagStack, line, indentation, inFunc, funcFirst, funcs, textNext
        
        if word is not '' and word.isspace() is False and indentation is not -2:
            if not inFunc:
                dprint('nw='+word)

                lineEmpty = line.isspace() or line is ''

                if lineEmpty:
                    tagStack.append(word)
                    dprint(str(indentation)+'tag+'+word)
                
                if not lineEmpty:
                    line = line.rstrip(' ')
                    line += ' '
                elif not word.startswith('`'):
                    line += '<'
                
                line += word
            else:
                dprint('inFunc : ' + word)
                if funcFirst:
                    dprint('funcName')
                    funcs.append(marksmolFunc(word,[],''))
                    funcFirst = False
                else:
                    if textNext:
                        dprint('funcText')
                        funcs[-1].text = word[1:]
                        inFunc = False
                        textNext = False
                        funcFirst = True
                    else:
                        dprint('funcVar')
                        funcs[-1].variables.append(word)
        word = ''

    def endLine():
        nonlocal code, word, tagStack, indentation, rootIndentation, line, inFunc

        if inFunc:
            return

        if line.isspace() or line is '':
            indentation = 0
            return

        dprint(str(rootIndentation)+'nl'+str(indentation))

        ptag = ''
        if len(tagStack) > 0:
            ptag = tagStack[-1]
        
        dprint('ptag:'+ptag)

        if not ptag.startswith('`'):
            line += '>'
            dprint('>ptag:'+ptag)

        if rootIndentation >= indentation:
            tag = getPrevTag()
           
            dprint('\tempty:'+tag)

            if tag.startswith('`') is False:
                code = code.rstrip('\n') + '</'+tag+'>\n' #if you want sameline
                #code = code.rstrip('\n') + '\t'*rootIndentation+'</'+empt+'>\n' #if you want newline
            

        while rootIndentation > indentation:
            tag = getPrevTag()
            dprint('\t\tNOT EMPTY:'+tag)
            rootIndentation -= 1
            if tag.startswith('`') is False:
                code += '\t'*rootIndentation+'</' + tag + '>\n'
            
        
        if line.startswith('`'):
            line = line[1:]

        code += '\t' * indentation + line + '\n'



        line = ''
        if indentation > rootIndentation:
            rootIndentation = indentation
        indentation = 0

    dprint("\n\n        Parsing in: " + path)

    l = 0
    while l < len(t):
        #dprint('l:'+t[l])
        if escapeNext:
            word += t[l]
            escapeNext = False
        elif inComment > 0:
            if t[l] is '}':
                inComment -= 1
                dprint('}')
            elif t[l] is '{':
                inComment += 1
                dprint('{')
        elif inQuotes > 0:
            if t[l] is '"' and inQuotes is 1:
                word+='"'
                endWord()
                inQuotes = 0
            elif t[l] is "'" and inQuotes is 2:
                word+="'"
                endWord()
                inQuotes = 0
            elif t[l] is '`' and inQuotes is 3:
                #word+='`'
                endWord()
                inQuotes = 0
                textNext = False
            elif t[l] is '\n' and inQuotes is 4:
                #word+='`'
                #endWord()
                #endLine()
                
                
                #t = t[:l+1] + word + t[l+1:]
                endWord()
                #word = ''
                endLine()
                inQuotes = 0
            elif t[l] is "\\":
                escapeNext = True
            else:
                word += t[l]
        else:
            if t[l] is '\t' and not inFunc:
                endWord()
                indentation += 1
            elif t[l] is '\n':
                endWord()
                endLine()
            elif t[l] is '$' and word is '':
                inFunc = True
                word = '$'
                dprint('$')
            elif t[l] is ',' and inFunc:
                endWord()
            elif t[l] is ':' and inFunc:
                endWord()
                dprint(':')
                funcEnd(l)
            elif t[l] is ';':
                endWord()
                preInd = indentation
                endLine() #keep indentation
                indentation = preInd
            elif t[l] is '<':
                endWord()
                preInd = indentation
                endLine() #keep indentation + 1
                indentation = preInd+1
            elif t[l] is '>':
                endWord()
                preInd = indentation
                endLine() #keep indentation
                indentation = preInd
                inQuotes = 4
                word = '`'
            elif t[l] is '=':
                endWord()
                line += '='
            elif t[l] is '#':
                endWord()
                line =  line.rstrip(' ') +  ' id='
            elif t[l] is '.':
                endWord()
                line = line.rstrip(' ') + ' class='
            elif t[l] is ' ':
                endWord()
            elif t[l] is '{':
                inComment += 1
                dprint('{')
            elif t[l] is '"':
                word='"'
                inQuotes = 1
            elif t[l] is "'":
                word="'"
                inQuotes = 2
            elif t[l] is '`':
                endWord()
                word = '`'
                inQuotes = 3
            elif t[l] is '\\' and inQuotes is not 4:
                escapeNext = True
            else:
                word += t[l]
        l += 1
    
    endWord()
    endLine()
    indentation = 0
    tagStack.append('`')
    line = '`'
    endLine()

    return code

def main():
    folder = ''
    rec = ''
    debug = 'y'

    for x in range(len(sys.argv)):
        if sys.argv[x] == '--folder':
            folder = sys.argv[x+1]
        if sys.argv[x] == '--rec':
            rec = sys.argv[x+1]
        if sys.argv[x] == '--debug':
            debug = sys.argv[x+1]
    
    if folder == '':
        folder = input("Folder/Root:")
    if rec == '':
        rec = input("Recursive (y/n):")

    rec = rec[0].lower()=="y"
    debug = debug[0].lower()=="y"

    files = []
    if rec is False:
        files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.ms')]
    else:
        for (dirpath, dirnames, filenames) in os.walk(folder):
            files.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.ms')])

    for f in files:
        txt = pathlib.Path(f).read_text()
        file = open(os.path.splitext(f)[0]+'.html','w')
        file.write(parse(txt,folder,debug))
        print(file.name)
        file.close()



if __name__ == '__main__':
    main()