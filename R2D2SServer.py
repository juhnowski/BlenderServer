bl_info = {
    'name': 'Socket Server',
    'author': 'Ilya Juhnowski',
    'version': (1, 1, 2),
    "blender": (2, 6, 1),
    "api": 12345,
    'location': 'Properties > Render',
    'description': 'Socket Server for communication with ZAK-57 client',
    'warning': 'It doesnt work without Target blender model. You need change parser implementation to fix it.',
    'wiki_url': 'none',
    'tracker_url': 'none',
    'category': 'Render'}
   

import bpy
import socket
import threading
import socketserver
import bgl
import math
global ss
global server

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        pi = 3.1415926
        data = self.request.recv(1024).decode("utf-8")
        #set response
        #response = "400 Internal Error"
        response = "200 Ok"
        cmd = data[0:3]
        if (cmd=="rx="):
            par = float(data[3:])
            fy = bpy.data.objects['Target'].rotation_euler[2]
            fz = bpy.data.objects['Target'].rotation_euler[0]
            par = par*pi/180
            bpy.data.objects['Target'].rotation_euler = (fz, par, fy)

        if (cmd=="fx="):
            par = float(data[3:])
            fx = bpy.data.objects['Target'].rotation_euler[1]
            fy = bpy.data.objects['Target'].rotation_euler[2]
            fz = bpy.data.objects['Target'].rotation_euler[0]
            par = par*pi/180
            bpy.data.objects['Target'].rotation_euler = (fz, fx+par, fy)
            
        if (cmd=="cx="):
            par = float(data[3:])
            fx = bpy.data.objects['Camera'].rotation_euler[1]
            fy = bpy.data.objects['Camera'].rotation_euler[2]
            fz = bpy.data.objects['Camera'].rotation_euler[0]
            par = par*pi/180
            bpy.data.objects['Camera'].rotation_euler = (fz, fx+par, fy)
        
        elif (cmd=="ry="):
            par = float(data[3:])
            fx = bpy.data.objects['Target'].rotation_euler[1]
            fz = bpy.data.objects['Target'].rotation_euler[0]
            par = par*pi/180
            bpy.data.objects['Target'].rotation_euler = (fz, fx, par)

        if (cmd=="fy="):
            par = float(data[3:])
            fx = bpy.data.objects['Target'].rotation_euler[1]
            fy = bpy.data.objects['Target'].rotation_euler[2]
            fz = bpy.data.objects['Target'].rotation_euler[0]
            par = par*pi/180
            bpy.data.objects['Target'].rotation_euler = (fz, fx, fy+par)

        if (cmd=="cy="):
            par = float(data[3:])
            fx = bpy.data.objects['Camera'].rotation_euler[1]
            fy = bpy.data.objects['Camera'].rotation_euler[2]
            fz = bpy.data.objects['Camera'].rotation_euler[0]
            par = par*pi/180
            bpy.data.objects['Camera'].rotation_euler = (fz, fx, fy+par)

        elif (cmd=="rz="):
            par = float(data[3:])
            fx = bpy.data.objects['Target'].rotation_euler[1]
            fy = bpy.data.objects['Target'].rotation_euler[2]
            par = par*pi/180
            bpy.data.objects['Target'].rotation_euler = (par, fx, fy)

        if (cmd=="fz="):
            par = float(data[3:])
            fx = bpy.data.objects['Target'].rotation_euler[1]
            fy = bpy.data.objects['Target'].rotation_euler[2]
            fz = bpy.data.objects['Target'].rotation_euler[0]
            par = par*pi/180
            bpy.data.objects['Target'].rotation_euler = (fz+par, fx, fy)

        if (cmd=="cz="):
            par = float(data[3:])
            fx = bpy.data.objects['Camera'].rotation_euler[1]
            fy = bpy.data.objects['Camera'].rotation_euler[2]
            fz = bpy.data.objects['Camera'].rotation_euler[0]
            par = par*pi/180
            bpy.data.objects['Camera'].rotation_euler = (fz+par, fx, fy)
       
        elif (cmd=="jx="):
            par = float(data[3:])
            y = bpy.data.objects['Target'].location[2]
            z = bpy.data.objects['Target'].location[0]
            bpy.data.objects['Target'].location = (z, par, y)

        elif (cmd=="jy="):
            par = float(data[3:])
            x = bpy.data.objects['Target'].location[1]
            z = bpy.data.objects['Target'].location[0]
            bpy.data.objects['Target'].location = (z, x, par)
                        
        elif (cmd=="jz="):
            par = float(data[3:])
            x = bpy.data.objects['Target'].location[1]
            y = bpy.data.objects['Target'].location[2]
            bpy.data.objects['Target'].location = (par, x, y)
            
        elif (cmd=="mx="):
            par = float(data[3:])
            x = bpy.data.objects['Target'].location[1]
            y = bpy.data.objects['Target'].location[2]
            z = bpy.data.objects['Target'].location[0]
            bpy.data.objects['Target'].location = (z, x+par, y)

        elif (cmd=="my="):
            par = float(data[3:])
            x = bpy.data.objects['Target'].location[1]
            y = bpy.data.objects['Target'].location[2]
            z = bpy.data.objects['Target'].location[0]
            bpy.data.objects['Target'].location = (z, x, y+par)

        elif (cmd=="mz="):
            par = float(data[3:])
            x = bpy.data.objects['Target'].location[1]
            y = bpy.data.objects['Target'].location[2]
            z = bpy.data.objects['Target'].location[0]
            bpy.data.objects['Target'].location = (z+par, x, y)

        elif (cmd=="i"):
            bpy.data.objects['Target'].rotation_euler = (0, 0, 0)            
            bpy.data.objects['Target'].location = (0, 0, 0)
            
        elif (cmd=="stop"):
            server.shutdown()
            response = "900 Server Shutdown"
            print("server shutdown")

        else :
            response = "401 Unknown command"
        print("send response")
        print(str.encode(response))
        self.request.send(str.encode(response))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    
class SServer():
    
    def __init__(self,host="0.0.0.0",port=9001):
        self.host = host
        self.port = port
        self.started = False
        print("SServer initialized")
        
    def __start__(self):
        print("Server start: start")
        global server
        server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        err=server_thread.start()
        print(err)
        self.started = True
        print ("Server loop running in thread:" + str(server_thread.name))
        print("Server start: done")
        
    def __stop__(self):
        global server
        print("Server shutdown: start")
        server.shutdown()    
        self.started = False
        print("Server shutdown: done")
    
    def __setHost__(self, host):
        if self.started:
            self.stop()
        self.host = host

    def __setPort__(self, port):
        if self.started:
            self.stop()
        self.port = port

ss = SServer()
print(ss)

class SServerStart(bpy.types.Operator):
    '''Socket Server Start'''
    bl_idname = "object.sserver_start"
    bl_label = "Socket Server Controller"
    global ss
    
    def execute(self, context):
        print("SServer start")
        print(ss)
        ss.__start__()
        return {'FINISHED'}

class SServerStop(bpy.types.Operator):
    '''Socket Server Stop'''
    bl_idname = "object.sserver_stop"
    bl_label = "Socket Server Stop"
    global ss
    def execute(self, context):
        print("SServer stop")
        print(ss)
        ss.__stop__()
        return {'FINISHED'}

class SSPanel(bpy.types.Panel):
    bl_label = "Socket Server"
    bl_idname = "OBJECT_SS_controller"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
            
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        rd = scene.render
        row = layout.row()
        global ss #= SServer()
    
        row.operator("object.sserver_start", text="start", icon='WORLD_DATA')
        row.operator("object.sserver_stop", text="stop", icon='WORLD_DATA')
        
        split = layout.split()
        col = split.column()
        row = col.row()
        row.label(text=str("Host: "+ss.host))
        
        split = layout.split()
        col = split.column()
        row = col.row()
        row.label(text=str("Port: "+str(ss.port)))

        split = layout.split()
        col = split.column()
        row = col.row()
        row.label(text=str("Is Started: "+str(ss.started)))
        
        split = layout.split()
        col = split.column()
        row = col.row()
        row.label(text=str("Version: "+str(bl_info['version'])))

def register():
    #bpy.context.object["SS_Host"] = "127.0.0.1"
    #bpy.context.object["SS_Port"] = 9001
    bpy.utils.register_class(SServerStart)
    bpy.utils.register_class(SServerStop)
    bpy.utils.register_class(SSPanel)


def unregister():
    bpy.utils.unregister_class(SSPanel)
    bpy.utils.unregister_class(SServerStart)
    bpy.utils.unregister_class(SServerStop)

if __name__ == "__main__":
    register()







