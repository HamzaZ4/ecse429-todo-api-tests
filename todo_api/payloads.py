from xml.etree import ElementTree


def todo_payload(title="payload todo", done_status=False, description=""):
    return {"title": title, "doneStatus": done_status, "description": description}


def todo_xml(title, done_status=None, description=None):
    todo = ElementTree.Element("todo")
    ElementTree.SubElement(todo, "title").text = title
    if done_status is not None:
        ElementTree.SubElement(todo, "doneStatus").text = str(done_status).lower()
    if description is not None:
        ElementTree.SubElement(todo, "description").text = description
    return ElementTree.tostring(todo, encoding="unicode")


def parse_xml(text):
    return ElementTree.fromstring(text)
