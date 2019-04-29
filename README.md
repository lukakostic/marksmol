## My small and simplified version of HTML, called marksmol

Still need to add includes, multiple language versions, options and a visual studio code extension


```html
<head>
    <meta charset= 'utf-8'></meta>
    <meta http-equiv= 'Content-Type' content= 'text/html; charset=utf-8'></meta>

    <title>
        Some title
    </title>

    <link rel= 'stylesheet' type= 'text/css' href= 'styles.css'></link>

    <script src= 'Script.js'></script>
    <script>
        alert('Inline code!');
    </script>
</head>
```
### Versus: 
```racket
head
    meta charset='utf-8'
    meta http-equiv='Content-Type' content='text/html; charset=utf-8'
    
    title
        `Some title`
        
    link rel='stylesheet' type='text/css' href='styles.css'
    
    script src='Script.js'
    script
        `alert('Inline code!');`
```
Bottom one is a bit more simpler and shorter id say.

# More Examples:

## Html:
```html
<body class= 'home'>
	<div id= 'main-content'>
		<div id= 'preload' style= 'display: none;'>
			<div class= 'kd-bounce'>Yo Waddup</div>
		</div>
		
		<div class= 'mobile'>
			<div class= 'container'>
				Hello!
				You can write text using ` and escape them using \
				so like this \`
			</div>
		</div>
	</div>
</body>
```

## Marksmol:
```racket
{
YOO
COMMENT!
}
body .'home'
    div #'main-content'
        div #'preload' style='display: none;'
            div .'kd-bounce'>Yo Waddup
        
        div .'mobile'
            div .'container'
                `Hello!
                You can write text using \` and escape them using \\
                so like this \\\``
```


The html was generated from marksmol

# Usage
Just start marksmol.py, you can then use it to generate html from marksmol (.ms) files

Non-recursive mode will generate .html from all .ms in a single folder,
recursive will do it for every folder & child folder in the root folder

It uses indentations instead of <> & </>

'&#35;' is turned into 'id='
'.' is turned into 'class='
(when outside strings)

You can write comments with { and } :
```
{
commnet
this too
}
```
or one line:
```
{ comment }
```

Newline shortcuts:

```
a
b

Is same as:

a;b

----------------

a
	b

Is same as:

a<b

----------------

a
	`Some Text`

Is same as:

a>Some Text

and as:

a<`Some Text`
```

```
'>' adds newline + tab + string (one line)
'<' adds newline + tab
```

## Templates/Functions

```
$hi $person $action:
`\`Hello $person, nice to $action you!\``

test
	$hi `Luka` `meet`:
	$hi `Bob` `see`:
```
results in:
```
<test>
	Hello Luka, nice to meet you!
	Hello Bob, nice to see you!
</test>
```


```
Quotes escaped so  the pased text would be:
`Hello $person, nice to $action you!`
if without then its not considered text:
Hello $person, nice to $action you!
and 'Hello' would become <Hello></Hello>
```

':' signifies an end of an function, if it was already declared then it pastes the content.

function names must start with '$' but its variables (eg '$person') dont. Tho since it does a simple replace, its recomended to make them unique (eg dont make it 'a' as then it will replace all a's in the text. '$a' is better.)

You can make nested functions:

```
$hi $person $action:
`$post \`Hi $person, nice to $action you!\`:`

$post $text:
`post
	a
		\`$text\``

test
	$hi `Luka` `meet`:
	$hi `Bob` `see`:
```
results in:
```
<test>
	<post>
		<a>
			Hi Luka, nice to meet you!
		</a>
	</post>
	<post>
		<a>
			Hi Bob, nice to see you!
		</a>
	</post>
</test>
```