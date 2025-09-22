import os
from string import Template


def render_template(template_name, context={}):
    template_path = os.path.join('templates', template_name)
    with open(template_path, 'r') as f:
        template_string = f.read()
    return Template(template_string).safe_substitute(context)


def guess_type(path):
    MIME_TYPES = {
        '.html': 'text/html',
        '.htm': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.pdf': 'application/pdf',
        '.zip': 'application/zip',
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.wav': 'audio/wav',
        '.mp3': 'audio/mpeg',
        '.ogg': 'audio/ogg',
    }
    base, ext = os.path.splitext(path)
    return MIME_TYPES.get(ext, 'application/octet-stream')