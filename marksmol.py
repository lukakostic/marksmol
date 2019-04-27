import os
import pathlib

def parse(t):
    code = ''
    word = ''
    line = ''
    inQuotes = 0
    inComment = False
    indentation = 0
    escapeNext = False
    tagStack = []
    rootIndentation = -1

    t = t.replace(' '*4, '\t').replace("\r\n",'\n')

        #DEBUG
    def dprint(txt):
        if False:
            print(txt)

    def getPrevTag():
        nonlocal tagStack

        tag = tagStack.pop()
        if len(tagStack) is not 0:
            retTag = tagStack.pop()
            tagStack.append(tag)
            return retTag
        return tag

    def endWord():
        nonlocal code, word, tagStack, line, indentation
        
        if word is not '' and word.isspace() is False and indentation is not -2:
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

        word = ''

            

    
    def endLine():
        nonlocal code, word, tagStack, indentation, rootIndentation, line

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
            

        code += '\t' * indentation + line.lstrip('`') + '\n'



        line = ''
        if indentation > rootIndentation:
            rootIndentation = indentation
        indentation = 0

        

    for l in range(len(t)):
        if escapeNext:
            word += t[l]
            escapeNext = False
        elif inComment:
            if t[l] is '}':
                inComment = False
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
            elif t[l] is '\n' and inQuotes is 4:
                #word+='`'
                endWord()
                endLine()
                inQuotes = 0
            elif t[l] is "\\":
                escapeNext = True
            else:
                word += t[l]
        else:
            if t[l] is '\t':
                endWord()
                indentation += 1
            elif t[l] is '\n':
                endWord()
                endLine()
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
                endLine() #keep indentation + 1
                indentation = preInd+1
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
                inComment = True
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
            elif t[l] is '\\':
                escapeNext = True
            else:
                word += t[l]
    
    endWord()
    endLine()
    indentation = 0
    tagStack.append('`')
    line = '`'
    endLine()

    return code

def main():
    folder = input("Folder/Root:")
    rec = input("Recursive (y/n):")[0].lower()=="y"

    files = []
    if rec is False:
        files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.ms')]
    else:
        for (dirpath, dirnames, filenames) in os.walk(folder):
            files.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.ms')])

    for f in files:
        txt = pathlib.Path(f).read_text()
        file = open(os.path.splitext(f)[0]+'.html','w')
        file.write(parse(txt))
        print(file.name)
        file.close()



if __name__ == '__main__':
    main()