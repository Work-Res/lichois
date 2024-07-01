mutiple_pages = """
<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Watermarks example</title>
<style>
    @page {
        size: a4 portrait;
        @frame header_frame {           /* Static Frame */
            -pdf-frame-content: header_content;
            left: 50pt; width: 512pt; top: 60pt; height: 250pt;
        }
        @frame content_frame {          /* Content Frame */
            left: 50pt; width: 512pt; top: 90pt; height: 632pt;
        }
        @frame footer_frame {           /* Another static Frame */
            -pdf-frame-content: footer_content;
            left: 50pt; width: 512pt; top: 760pt; height: 20pt;
        }
    }
</style>
</head>

<body>
    <!-- Content for Static Frame 'header_frame' -->
    <div id="header_content">
         <div class="container">
            <img src="{{ image_url }}" alt="Logo" width="200px" height="200px">
        </div>
    </div>

    <!-- Content for Static Frame 'footer_frame' -->
    <div id="footer_content">(c) - page <pdf:pagenumber>
        of <pdf:pagecount>
    </div>

    <!-- HTML Content -->
   
</body>


</html>
"""