# Java Extensible Language
The programming language that has the syntax of XML and the power of Java and Python combined.

```
<JXL>
	<main>
		<print>"Hello World!"</print>
	</main>
</JXL>
```

[Check out the JXL Wiki and start playing!](https://github.com/EricsonWillians/JXL/wiki)

#### Current Language Progress
* Scopes.
* Native Python data types.
* JXL variable creation and access.
* Native Unicode support for JXL variable creation and access.
* Expression evaluation using Python by default.
* JXL variable access from within python expressions.
* Python statements within JXL using the python keyword tag.
* JXL variable access from within python statements.

#### Technical Details

JXL is a programming language that has an interpreter ([JXLInterpreter](https://github.com/EricsonWillians/JXL/blob/master/JXLInterpreter.py)) that executes code written in XML. It relies heavily on the [Document Object Model API](http://docs.oracle.com/javase/7/docs/api/org/w3c/dom/package-summary.html) of the [Java API for XML Processing](http://java.sun.com/xml). The whole code is being written in the [Python Programming Language](http://python.org/) using [Jython](http://www.jython.org/), and my aim is to grant access to both Python and Java from inside the XML file.
