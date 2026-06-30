<!DOCTYPE html>
<html>
    <head>
        <style>
            body {
                background-color: #ffffff;
                color: #636363;
                margin:0;
            }
            header {
                height: 110px;
                width: 100vw;
                font-size: 20px;
            }
            .heading {
                padding: 5px;
            }
            #SOPSearch {
                background-color: #338654;
                color: #000000;
                width: 100vw;
                padding: 25px;
            }

        </style>
        <title>SOP Search</title>
    </head>
    <body>
        <header>
            <h1 class="heading">SOP Search</h1>
            <b class="heading">By Canon Sparks</b>
        </header>
        <div id="SOPSearch">
            <form action="search.php">
                <label for="SOPS">Search SOPs:</label>
                <input type="search" id="SOPS" name="SOPS"></input>
            </form>
        </div>
    </body>
</html>