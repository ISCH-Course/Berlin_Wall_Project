<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="1.0">

    <!-- Match TEI root element -->
    <xsl:template match="tei:TEI">
        <html>
            <head>
                <title>
                    <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
                </title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        background-color: #f2f2f2;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #fff;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                        border-radius: 5px;
                    }
                    .metadata {
                        border-bottom: 1px solid #ccc;
                        padding-bottom: 10px;
                        margin-bottom: 20px;
                    }
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    h1, h2 {
                        color: #333;
                    }
                    .speech {
                        margin-top: 20px;
                    }
                    .speaker {
                        font-weight: bold;
                        color: #007bff;
                    }
                    .dialogue {
                        margin-left: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <!-- Metadata -->
                    <div class="metadata">
                        <h1>
                            <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
                        </h1>
                        <p>
                            <b>Encoded by: </b>
                            <xsl:for-each select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:respStmt/tei:name">
                                <xsl:value-of select="."/>
                                <xsl:if test="position() != last()">, </xsl:if>
                            </xsl:for-each>
                        </p>
                        <p>
                            <b>Publisher: </b>
                            <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:publisher"/>
                        </p>
                        <p>
                            <b>Publication Place: </b>
                            <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:pubPlace"/>
                        </p>
                        <p>
                            <b>Date: </b>
                            <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:date"/>
                        </p>
                    </div>
                    <!-- Speech -->
                    <h2>
                        <xsl:value-of select="tei:text/tei:body/tei:div/tei:head"/>
                    </h2>
                    <div class="speech">
                        <xsl:apply-templates select="tei:text/tei:body/tei:div/tei:sp"/>
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>

    <!-- Convert speaker and dialogue -->
    <xsl:template match="tei:sp">
        <div>
            <p class="speaker"><xsl:value-of select="tei:speaker"/></p>
            <xsl:apply-templates select="tei:p"/>
        </div>
    </xsl:template>

    <!-- Convert paragraphs -->
    <xsl:template match="tei:p">
        <p class="dialogue"><xsl:value-of select="."/></p>
    </xsl:template>

</xsl:stylesheet>
