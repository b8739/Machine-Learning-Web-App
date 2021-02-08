<template>
    <header>
    <nav>
        <a href="#">Datasets</a>
        <a href="#">Preprocess</a>
        <a href="#">EDA</a>
        <a href="#">Modeling</a>
        <a href="#">Optimize</a>
    </nav>
    </header>
</template>

<style>
    /* reset */
*{
    font-family: 'Poppins', sans-serif;
}
#dataTable td:hover{
    background-color: #ececff;
    cursor: pointer;
}
a{
  text-decoration: none;
}
/* base.html */
header nav{
	text-align: center;
	height: 60px;
	background-color: #87ceeb;
}
header nav a{
	display:inline-block;
	font-family: 'Noto Sans JP', sans-serif;
	color: #FAFAFA;
  margin:13px 60px 0 0;
  font-size: 20px;
}
/* index.html */
body{
    font:15px/1.5 Arial, Helvetica,sans-serif;
  }
.fileUploader{
  width: 400px;
  height: 400px;
  margin: 0 auto;
  background-color: #87ceeb;
}
.inputfile {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}
.inputfile + label {
  max-width: 80%;
  font-size: 1.25rem;
  /* 20px */
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
  display: inline-block;
  overflow: hidden;
  padding: 0.625rem 1.25rem;
  /* 10px 20px */
}
.inputfile:focus + label,
.inputfile.has-focus + label {
    outline: 1px dotted #000;
    outline: -webkit-focus-ring-color auto 5px;
}


.inputfile + label svg {
    width: 1em;
    height: 1em;
    vertical-align: middle;
    fill: currentColor;
    margin-top: -0.25em;
    /* 4px */
    margin-right: 0.25em;
    /* 4px */
}

.uploadGuide{
  text-align: center;
}
/* style 1 */

.inputfile-1 + label {
    color: #f1e5e6;
    background-color: #d3394c;
}

.inputfile-1:focus + label,
.inputfile-1.has-focus + label,
.inputfile-1 + label:hover {
    background-color: #722040;
}

</style>