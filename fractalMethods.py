import numpy as np
import bpy
import mathutils
from math import pi
import random
import time

"""
This library contains methods common between fractal generator scripts in the project, such as
angle operations and object manipulations.
"""

#### EULER ANGLE OPERATIONS ##################
def eulerMatrix(
        rotEuler):  # this function generates the transformation matrix for the coordinate system based on an XYZ euler rotation
    a = rotEuler[0]
    b = rotEuler[1]
    c = rotEuler[2]
    return ([[cos(b) * cos(c), -cos(b) * sin(c), sin(b)],
             [cos(a) * sin(c) + sin(a) * sin(b) * cos(c), cos(a) * cos(c) - sin(a) * sin(b) * sin(c), -sin(a) * sin(b)],
             [sin(a) * sin(c) - cos(a) * sin(b) * cos(c), sin(a) * cos(c) + cos(a) * sin(b) * sin(c), cos(a) * cos(b)]])

def eulerAngleExtraction(rotMat):  # extracts angles out of an euler matrix(inverse of eulerMatrix)
    angleVector = [0, 0, 0]
    angleVector[0] = np.arctan2(rotMat[1][2], rotMat[2][2])
    angleVector[1] = np.arctan2(-rotMat[0][2], ((rotMat[0][0]) ** 2 + (rotMat[0][1]) ** 2) ** 0.5)
    angleVector[2] = np.arctan2(sin(angleVector[0]) * rotMat[2][0] - cos(angleVector[0]) * rotMat[1][0],
                                cos(angleVector[0]) * rotMat[1][1] - sin(angleVector[0]) * rotMat[2][1])
    return angleVector


#### QUATERNION OPERATIONS ################
def quatMatrix(rotQuat):  #Generates rotation matrix from a quaternion
    a = rotQuat[0]
    b = rotQuat[1]
    c = rotQuat[2]
    d = rotQuat[3]
    #see https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Conversion_to_and_from_the_matrix_representation
    return ([[a ** 2 + b ** 2 - c ** 2 - d ** 2, 2 * b * c - 2 * a * (d), 2 * b * d + 2 * a * c], \
             [2 * b * c + 2 * a * d, (a ** 2 - b ** 2 + c ** 2 - d ** 2), (2 * c * d - 2 * a * b)], \
             [2 * b * d - 2 * a * c, 2 * c * d + 2 * a * b, a ** 2 - b ** 2 - c ** 2 + d ** 2]])

def quatValueExtraction(rotMat):  #Generates a rotation quaternion from a rotation matrix
    quatVector = [0, 0, 0, 0]
    #see https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Conversion_to_and_from_the_matrix_representation
    quatVector[0] = 0.5 * (1 + rotMat[0][0] + rotMat[1][1] + rotMat[2][2]) ** 0.5
    quatVector[1] = (rotMat[2][1] - rotMat[1][2]) / (4 * quatVector[0])
    quatVector[2] = (rotMat[0][2] - rotMat[2][0]) / (4 * quatVector[0])
    quatVector[3] = (rotMat[1][0] - rotMat[0][1]) / (4 * quatVector[0])
    return quatVector


#### OBJECT MANIPULATION ############################
def dupe(bpyObject, newName):  # copies object argument and inserts it into the scene as an unlinked object
    newObj = bpyObject.copy() #duplicates object
    newObj.name = newName #sets duplicate name
    bpy.data.scenes[0].objects.link(newObj) #puts object in scene
    newObj.data = bpyObject.data.copy() #copy over object data
    return newObj

def diff(nameMain,nameMask):
    '''
    This method takes the difference between a main and mask mesh, and yields only what's left of the main mesh,
    deleting the mask
    '''
    
    bpy.ops.object.select_all(action='DESELECT') #make sure nothing is selected
    bpy.data.objects[nameMain].select = True #select main object
    bpy.context.scene.objects.active = bpy.data.objects[nameMain] #set main object as active object
    
    bpy.ops.object.modifier_add(type='BOOLEAN') #add a boolean modifier to the object
    
    mods = bpy.data.objects[nameMain].modifiers #get a list of active modifiers of the object
    mods[0].name = "CurSub"
    mods[0].object = bpy.data.objects[nameMask] #set the mask object as the object of the modifier
    mods[0].operation = 'DIFFERENCE' #set operation to difference, it is intersect by default
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mods[0].name) #apply the modifier
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[nameMask].select = True #select mask object
    bpy.context.scene.objects.active = bpy.data.objects[nameMask] #set mask object as active object, i'm not sure this is necessary****
    bpy.ops.object.delete() #delete mask
    
def union(nameMain,nameMask):
    '''
    This method takes the union between a main and mask mesh.
    '''
    
    bpy.ops.object.select_all(action='DESELECT') #make sure nothing is selected
    bpy.data.objects[nameMain].select = True #select main object
    bpy.context.scene.objects.active = bpy.data.objects[nameMain] #set main object as active object
    
    bpy.ops.object.modifier_add(type='BOOLEAN') #add a boolean modifier to the object
    
    mods = bpy.data.objects[nameMain].modifiers #get a list of active modifiers of the object
    mods[0].name = "CurSub"
    mods[0].object = bpy.data.objects[nameMask] #set the mask object as the object of the modifier
    mods[0].operation = 'UNION' #set operation to difference, it is intersect by default
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mods[0].name) #apply the modifier
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[nameMask].select = True #select mask object
    bpy.context.scene.objects.active = bpy.data.objects[nameMask] #set mask object as active object, i'm not sure this is necessary****
    bpy.ops.object.delete() #delete mask
    
def remesh(nameMain):
    '''
    Applies the remesh modifier to the selected object. Don't use this method, it doesn't work... :(
    '''
        
    bpy.ops.object.select_all(action='DESELECT') #make sure nothing is selected
    bpy.data.objects[nameMain].select = True #select main object
    bpy.context.scene.objects.active = bpy.data.objects[nameMain] #set main object as active object
    
    bpy.ops.object.modifier_add(type='REMESH') #add a boolean modifier to the object
    
    mods = bpy.data.objects[nameMain].modifiers #get a list of active modifiers of the object
    mods[0].name = "CurRemesh"
    mods[0].octree_depth = 4 #resolution of octree, probably avoid going higher than 8
    mods[0].mode = 'SHARP' #tries to reproduce sharp edges, 'BLOCKS' also has decent results
    mods[0].sharpness = 1 #i'm not sure what this number represents, but bigger means edges preserved better
    
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mods[0].name) #apply the modifier