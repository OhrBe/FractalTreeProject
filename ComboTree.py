import os
import sys

import bpy
import mathutils

FolderPath = os.path.dirname(os.path.abspath('ComboTree.py'))  # get directory of script
sys.path.append(FolderPath)  # add directory to python module filepath
from fractalMethods import *

"""
tree lists are in the format treelist = [angle1,angle2,xAngle1,xAngle2,twist1,twist2,height,width,scaleFactor]
                                          0      1       2       3       4      5      6      7       8
xAngle, angle, and twist refer to the Euler X, Y and Z angles respectively.
"""


# TREE GEN METHODS ########################################

def treeListCombo(ratio, tree1, tree2):
    nratio = 1 - ratio  # the ratios must add up to 1, so take a complement
    comboTree = []
    for i in range(9):
        comboTree.append(ratio * tree1[i] + nratio * tree2[i])  # ratio is the weight of tree1, the rest is tree2
    return comboTree


def treeTransform(objSegment, binaryPosition, xAngle, angle, twist, height, width,
                  scaleFactor):  # this function places duplicate edge loops at relevant postition with the relevant rotation

    prescale = objSegment.scale[0]  # set new object to same scale just in case
    objSegment.scale = [scaleFactor * prescale, scaleFactor * prescale,
                        scaleFactor * prescale]  # scale object in xyz by scale factor

    if twist == 'RAND':  # random number generators used in testing, doesn't produce interesting structures
        twist = pi / random.randint(2, 24)
    if angle == 'RAND':
        angle = pi / random.randint(4, 24)
    if xAngle == 'RAND':
        xAngle = pi / random.randint(4, 24)

    if binaryPosition == 1:  # Binary postion is how the tree is organized and generated. See fractal document.
        objSegment.location = np.asarray(objSegment.location) + np.dot(quatMatrix(objSegment.rotation_quaternion),
                                                                       [0, width * prescale, height * prescale])
        # move the object to the current location plus the dot product of the rotation matrix and the translation matrix,
        # this has the effect of moving the object with reference to the direction the parent is facing

        objSegment.rotation_quaternion = quatValueExtraction(np.dot(quatMatrix(objSegment.rotation_quaternion),
                                                                    quatMatrix(mathutils.Euler((xAngle, angle, twist),
                                                                                               'XYZ').to_quaternion())))
        # Sets the quaternion rotation based on the dot product of the current rotation matrix with the desired rotation
        # matrix, calculated from the euler angles supplied by the user. Program uses Quaternions as Euler angles have
        # very serious floating point precision issues at angles close to pi/2.

    else:  # same process as for 1, except some rotations and translations in opposite direction to create branching
        objSegment.location = np.asarray(objSegment.location) + np.dot(quatMatrix(objSegment.rotation_quaternion),
                                                                       [0, -width * prescale, height * prescale])

        objSegment.rotation_quaternion = quatValueExtraction(np.dot(quatMatrix(objSegment.rotation_quaternion),
                                                                    quatMatrix(mathutils.Euler((xAngle, -angle, twist),
                                                                                               'XYZ').to_quaternion())))


def specialSegGen(edgeLoop, ratioMulti, cuts, shape, currentIter, tree1, tree2):
    loopName = edgeLoop.name  # store name of current edge loop
    SegA = dupe(edgeLoop, loopName + '1')  # duplicate current edge loop to make bottom edge
    SegB = dupe(edgeLoop, loopName + '2')
    newSegA = dupe(SegA, loopName + '1x')  # duplicate SegA to create top edge
    newSegB = dupe(SegB, loopName + '2x')

    positionA = SegA.name[
                -currentIter - 1:]  # find the binary positions of these segments to determine scaling and rotation
    positionB = SegB.name[-currentIter - 1:]
    ratioA = positionA.count('1') / len(positionA)  # calculates weights for each tree list for each segment
    ratioB = positionB.count('1') / len(positionB)

    comboA = treeListCombo(ratioMulti * ratioA, tree1, tree2)  # generate the angles and positions of this segment
    comboB = treeListCombo(ratioMulti * ratioB, tree1,
                           tree2)  # ratioMulti was added just to play around with changing weights
    treeTransform(newSegA, 1, comboA[2], comboA[0], comboA[4], comboA[6], comboA[7],
                  comboA[8])  # move the ends to relevant
    treeTransform(newSegB, 2, comboB[3], comboB[1], comboB[5], comboB[6], comboB[7], comboB[8])  # postitions
    nextSegA = dupe(newSegA, SegA.name + '1')  # name the segments
    nextSegB = dupe(newSegB, SegB.name + '2')

    bpy.ops.object.select_all(action='DESELECT')  # deselect to be safe
    newSegA.select = True  # select top end of A
    SegA.select = True  # select bottom end of A
    bpy.context.scene.objects.active = SegA  # set bottom end as the active object
    bpy.ops.object.join()  # join top and bottom edge loops to a single mesh object
    bpy.ops.object.mode_set(mode='EDIT')  # switch to edit mode
    bpy.ops.mesh.bridge_edge_loops(number_cuts=cuts, profile_shape=shape)  # connect top and bottom loops with polygons
    bpy.ops.object.mode_set(mode='OBJECT')  # return to object mode

    bpy.ops.object.select_all(action='DESELECT')  # same connecting process as for SegA
    newSegB.select = True
    SegB.select = True
    bpy.context.scene.objects.active = SegB
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bridge_edge_loops(number_cuts=cuts, profile_shape=shape)
    bpy.ops.object.mode_set(mode='OBJECT')

    return (nextSegA.name, nextSegB.name)  # return names to add to lists in tree bridge method


def specialTreeBridge(tree1, tree2, ratioMulti=1, startingPoint=(0, 0, 0), cuts=0, shape='SMOOTH', iterations=5):
    bpy.ops.mesh.primitive_circle_add(location=startingPoint, fill_type='TRIFAN')  # create initial edge loop
    startSeg = bpy.context.object  # mark the currently selected initial edge loop as the first segment
    startSeg.rotation_mode = "QUATERNION"  # set rotation mode to quaternion

    bpy.ops.object.select_all(action='DESELECT')  # deselect all objects
    listAll = [[startSeg.name]]  # create a 2d list with the first element being the first segment
    for iter in range(iterations):
        listAll.append([])  # add the next layer's list
        listLayer = listAll[iter + 1]  # assign next layer's list to variable
        listRef = listAll[iter]  # assign previous layer's list to variable

        for segName in listRef:  # iterate through objects in previous layer
            # position = listRef.index(segName)
            tupSegs = specialSegGen(bpy.data.objects[segName], ratioMulti, cuts, shape, iter, tree1, tree2)
            # Generate two segments produced by the current object by calling specialSegGen, store segment names in variable
            listLayer.append(tupSegs[0])  # add segment names to current layer, to reference for the next one
            listLayer.append(tupSegs[1])


# Main Script ##########################

if __name__ == '__main__':
    datafile = open(FolderPath + '/TreeData.txt', 'r')  # get data from data files generated by main script
    data = datafile.read()
    datafile.close()

    dataA, dataB = data.split('\n')

    # lstA = [X1,Y1,Z1,scale1,h1,w1,iterations]
    # lstB = [X2,Y2,Z2,scale2,h2,w2,iterations]
    X1, Y1, Z1, scale1, h1, w1, numIters = map(float, dataA.split(','))
    X2, Y2, Z2, scale2, h2, w2, ignore = map(float, dataB.split(','))

    Y1 *= (2 * pi / 360)  # convert degrees to radians
    Y2 *= (2 * pi / 360)
    X1 *= (2 * pi / 360)
    X2 *= (2 * pi / 360)
    Z1 *= (2 * pi / 360)
    Z2 *= (2 * pi / 360)

    treeListA = [Y1, Y1, X1, X1, Z1, Z1, h1, w1, scale1]  # set the data in lists
    treeListB = [Y2, Y2, X2, X2, Z2, Z2, h2, w2, scale2]

    '''
    tree lists are in the format treelist = [angle1,angle2,xAngle1,xAngle2,twist1,twist2,height,width,scaleFactor]
                                              0      1       2       3       4      5      6      7       8
    '''

    bpy.ops.wm.open_mainfile(filepath='./BlendFiles/TreeScene.blend')  # open the default scene

    currentTime = time.strftime('%y%m%d-%H%M%S', time.localtime())  # get current time in date-time format

    bpy.context.scene.render.filepath = './Renders/Tree{}.jpg'.format(currentTime)  # set the render image filepath
    specialTreeBridge(treeListA, treeListB, iterations=int(numIters))  # generate the tree
    bpy.ops.wm.save_as_mainfile(
        filepath='./BlendFiles/Tree{}.blend'.format(currentTime))  # save the generated tree to a blend file
    bpy.ops.render.render(write_still=True)  # render the image
