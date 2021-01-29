import io
import datetime
from fastapi import FastAPI
from starlette.responses import StreamingResponse, Response
from screenshot import Screenshot

app = FastAPI()


@app.get('/')
def screenshot(url: str):
    if url:
        s = Screenshot(url)
        png = s.get_image()
        if png:
            name = "%s.png" % str(datetime.datetime.now().time())
            return StreamingResponse(io.BytesIO(png), media_type="image/png")

    return Response(content="Error", status_code=404)
