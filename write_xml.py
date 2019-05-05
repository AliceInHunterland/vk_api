try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser
import xml.dom.minidom as md


#tree = ET.parse('xmlsample1.xml', ET.XMLParser(encoding='utf-8'))
#root= tree.getroot()
#ET.dump(tree)
#print(root[0][1].attrib)
#print(root)
#for child in root:
#    print (child.tag, child.attrib)
#for i in range(2):
#   print(root[0][i].text)

#for rank in root.iter('Text'):
#    new_rank = rank.text
#    rank.text = str(new_rank)+' Vacia'
#    rank.set('updated', 'yes')

#tree.write('output.xml')

#ov.write('output.xml')
#ok=ET.parse(a)
#ET.XML(a, parser=None)
#print(ET.fromstring(a))
users_list = ["Group1User1", "Group1User2", "Group2User1", "Group2User2"]




root = ET.Element("Root")
appt = ET.Element("Item")
root.append(appt)
    
    # создаем дочерний суб-элемент. 
ID = ET.SubElement(appt, "ID")
ID.text = "1181251680"
    
Header = ET.SubElement(appt, "Header")
Header.text = "040000008200E000"
    
Body = ET.SubElement(appt, "Body")
Body.text = "1181572063"
    
Username = ET.SubElement(appt, "Username")
    
UserID = ET.SubElement(appt, "UserID")
    
Confirmed = ET.SubElement(appt, "Confirmed")
Confirmed.text = "1800"
    
Date= ET.SubElement(appt, "Date")
    
Request = ET.SubElement(appt, "Request")
    
tags = ET.SubElement(appt, "Tags")
    
tag = ET.SubElement(tags, "Tag")

    
details = ET.SubElement(appt, "Details")
    
emotions = ET.SubElement(details, "Emotions")

emotion_l = ET.SubElement(emotions, "Emotion")
emotion_l.set('updated', 'like')
userID= ET.SubElement(emotion_l, "userID")

reposters = ET.SubElement(details, "Reposters")

comments = ET.SubElement(details, "Comments")

comment = ET.SubElement(comments, "Comment")

username=ET.SubElement(comment, "Username")
userid=ET.SubElement(comment, "UserID")
text=ET.SubElement(comment, "Text")

tree = ET.ElementTree(root)
xmlstr = md.parseString(ET.tostring(root)).toprettyxml(indent="           ")
with open("appt.xml", "w") as f:
         f.write(xmlstr)

 
if __name__ == "__main__":
    createXML()
