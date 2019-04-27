# marksmol
My small and simplified version of HTML, called marksmol


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
vs
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

## Html:
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

<body class= 'home'>
	<div id= 'main-content'>
		<div id= 'preload' style= 'display: none;'>
			<div class= 'kd-bounce'></div>
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
head
    meta charset='utf-8'
    meta http-equiv='Content-Type' content='text/html; charset=utf-8'
    
    title
        `Some title`
        
    link rel='stylesheet' type='text/css' href='styles.css'
    
    script src='Script.js'
    script
        `alert('Inline code!');`

body .'home'
    div #'main-content'
        div #'preload' style='display: none;'
            div .'kd-bounce'
        
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

Still need to add templates, multiple language versions, options and a visual studio code extension
