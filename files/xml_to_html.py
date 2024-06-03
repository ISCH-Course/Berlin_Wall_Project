from lxml import etree

# Load XML input and XSLT stylesheet
xml_doc = etree.parse("Reagan_speech.xml")
xslt_doc = etree.parse("stylesheet.xslt")

# Create an XSLT transformer
transform = etree.XSLT(xslt_doc)

# Apply the transformation
result_tree = transform(xml_doc)

# Output the transformed HTML to a new file
with open("Reagan_speech.html", "wb") as f:
    f.write(etree.tostring(result_tree, pretty_print=True))
