$hi $text:
`\`Hi $text!\``

a
	$hi >Hello!
:
{: in new line because > scans whole line}



a
	$hi `Hello!`:
	

$join $a $b:
`\`$a$b\``

a
    $join >Some
	> Text
	:

a
    $join >Some
	> Text
:

{indentation doesnt matter after the function name ($join) till :}

a< $join `Some` `Text`: