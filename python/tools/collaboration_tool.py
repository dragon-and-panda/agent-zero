from python.helpers.tool import Tool, Response
from python.collaboration import documents, socketio

class CollaborationTool(Tool):
    async def execute(self, action, content="", doc_id="default", **kwargs):
        if action == "read":
            text = documents.get(doc_id, "")
            return Response(message=f"Document content:\n{text}", break_loop=False)
        
        elif action == "write":
            # Overwrite
            documents[doc_id] = content
            socketio.emit('document_updated', {'content': content}, room=doc_id)
            return Response(message="Document updated.", break_loop=False)
            
        elif action == "append":
            current = documents.get(doc_id, "")
            new_content = current + "\n" + content
            documents[doc_id] = new_content
            socketio.emit('document_updated', {'content': new_content}, room=doc_id)
            return Response(message="Appended to document.", break_loop=False)

        else:
             return Response(message="Unknown action. Use read, write, or append.", break_loop=False)
