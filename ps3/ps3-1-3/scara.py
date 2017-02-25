import sys, os, time, pdb, collections, inspect
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.path import Path
import matplotlib.patches as patches


plt.ion()

b_pos = np.r_[800.0, 0.0, 0.0]
h_pos = np.r_[300.0, 0.0, 100.0]
c_pos = np.r_[300.0, 0.0, 100.0]

l0 = 500.0
l1 = 500.0

obj_array = []

# Globals.. avoid -.-"
link_config = [[[b_pos[0], b_pos[1], 500.0], [0.0, 1.0, 0.0], l0],
               [[b_pos[0], l0, 500.], [0.0, 1.0, 0.0], l1],
               [[b_pos[0], l0+l1, 500.], [0.0, 0.0, 1.0], 550]]


l3_offset = [0.0, 0.0, -116.0]  # link 3 offset in z axis
end_eff = [[0, 0, 0], [0.0, 1.0, 0.0], 50.0] # for visual purpose only. extension @ end-effector

joint_rad = [75, 42, 60]
base = [(b_pos[0]-75, b_pos[1]-75), 150, 150]  # [[x,y], width, height]
table = [(0., 0.), 500]  # [[x,y], radius]
joint_color = [0.8, 0.8, 0.8]
joint_edge_color = [0.8, 0, 0]

#object color
r_color = [1.0, 0.0, 0.0]
g_color = [0.0, 1.0, 0.0]
o_color = [0., 0., 0.]
a_value = 0.5

S1_BLIND = np.r_[-65.0, -115.0]
S2_BLIND = np.r_[-55, -125]
Z_LIMIT = np.r_[46.0, 546.0]

def buildJoints(scara_config=link_config, plt_fig=None):
    """
    :param scara_config: config of the robot as shown in 'link_config'
    :param plt_fig: figure handle to plot joints
    :return: figure handle of rendered plot
    """
    if plt_fig is None:
        plt_fig = plt.figure()
        plt_fig.add_subplot(111, projection='3d')

    ax = plt_fig.axes[0]
    rot_object = []

    # PS3/4
    
    # table
    table_obj = patches.Wedge(table[0],table[1], -90., 90., facecolor=joint_color, linewidth=0.9, edgecolor = joint_edge_color, linestyle='solid', fill=False)
    ax.add_patch(table_obj)
    art3d.pathpatch_2d_to_3d(table_obj, z=0)

    # OBJECT
    for obj in obj_array:
        if obj['o_type'] == 'R':
            r_obj = patches.Circle((obj['pos_x'], obj['pos_y']), 25.0, facecolor=r_color, linewidth=0.9, edgecolor = o_color, linestyle='solid', alpha=a_value)
            ax.add_patch(r_obj)
            art3d.pathpatch_2d_to_3d(r_obj, z=5.)
        elif obj['o_type'] == 'G':
            g_obj = patches.Circle((obj['pos_x'], obj['pos_y']), 50.0, facecolor=g_color, linewidth=0.9, edgecolor = o_color, linestyle='solid', alpha=a_value)
            ax.add_patch(g_obj)
            art3d.pathpatch_2d_to_3d(g_obj, z=5.)
            
        
    #  static base
    base_obj = patches.Rectangle(xy=base[0], width=base[1], height=base[2], facecolor=joint_color, edgecolor = joint_edge_color, linewidth=0.9)
    ax.add_patch(base_obj)
    art3d.pathpatch_2d_to_3d(base_obj, z=0)

    #  rot joints
    origin_x = link_config[0][0]
    for ix, l_conf in enumerate(scara_config):

        #buffer_xyz = np.r_[l_conf[0]]
        buffer_xyz = origin_x
        buffer_obj = patches.Circle((buffer_xyz[0], buffer_xyz[1]), joint_rad[ix], facecolor=joint_color, linewidth=0.9, edgecolor = joint_edge_color, linestyle='solid', alpha=a_value)
        rot_object.append(buffer_obj)

        ax.add_patch(rot_object[ix])
        art3d.pathpatch_2d_to_3d(rot_object[ix], z=buffer_xyz[2])
        origin_x = origin_x + np.r_[l_conf[1]]*np.r_[l_conf[2]]

    #  plot view config
    ax.set_xlim3d(b_pos[0]-1000, b_pos[0] + 1000)
    ax.set_ylim3d(b_pos[1]-1000, b_pos[1] + 1000)
    ax.set_zlim3d(b_pos[2], b_pos[2] + 1000)

    return plt_fig

def buildLinks(scara_config = link_config, plt_fig = None, end_effector = end_eff, z_shift = 0, theta = 0):

    if plt_fig is None:
        plt_fig = plt.figure()
        plt_fig.add_subplot(111, projection='3d')
    ax = plt_fig.axes[0]

    # base link
    #base_link = np.vstack((np.r_[0.0, 0.0, 0.0], scara_config[0][0]))
    base_link = np.vstack((b_pos, scara_config[0][0]))
    ax.plot(base_link[:, 0], base_link[:, 1], base_link[:, 2], 'b', linewidth=1.8)

    # plot links
    for ix, l_conf in enumerate(scara_config):

        buffer_origin = np.r_[l_conf[0]]
        buffer_vec = np.r_[l_conf[1]]
        buffer_mag = np.r_[l_conf[2]]
        buffer_end = buffer_origin + buffer_mag*buffer_vec
        link_pt_array = np.vstack((buffer_origin, buffer_end))
        if ix == 2:
            link_pt_array = link_pt_array + l3_offset + np.r_[0,0, -1*z_shift]

        ax.plot(link_pt_array[:, 0], link_pt_array[:, 1], link_pt_array[:, 2], 'b', linewidth=1.8 )

    # plot end effector
    end_effector_origin = link_pt_array[0, :]
    end_effector_end = end_effector_origin + np.r_[end_effector[1]]*np.r_[end_effector[2]]
    end_effector_array = np.vstack((end_effector_origin, end_effector_end))

    ax.plot(end_effector_array[:, 0], end_effector_array[:, 1], end_effector_array[:, 2], 'g', linewidth=1.8)

    #ax.text2D(0.98, 0.85, 'End-Effector position \nX: %d\nY: %d\nZ: %d\ntheta: %0.2f'% (end_effector_end[0], end_effector_end[1],
    #                                                                                 end_effector_end[2], theta),
    #        verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, color='black', fontsize=12)
    ax.text2D(0.98, 0.85, 'End-Effector position \nX: %.1f\nY: %.1f\nZ: %.1f\ntheta: %0.2f'% (end_effector_origin[0], end_effector_origin[1],
                                                                                        end_effector_origin[2], theta),
            verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, color='black', fontsize=12)
    #  plot view config
    ax.set_xlim3d(b_pos[0]-1000, b_pos[0]+200)
    ax.set_ylim3d(b_pos[1]-700, b_pos[1]+700)
    ax.set_zlim3d(b_pos[2],   b_pos[2]+700)
    # labels
    ax.set_xlabel('X_axis')
    ax.set_ylabel('Y_axis')
    ax.set_zlabel('Z_axis')
    plt.title('Scara Simulator')

    plt.show()


    return plt_fig

def plotSkeleton(robot_config = link_config, z_shift = 0, e_eff = end_eff, fig = None, theta=None):

    # build the joints and links
    if fig is None:
        plt_fig = plt.figure()
        plt_fig.add_subplot(111, projection='3d')
    else:
        plt_fig = fig

    plt_fig = buildJoints(scara_config=robot_config,plt_fig=plt_fig)
    plt_fig = buildLinks(scara_config=robot_config, z_shift = z_shift, plt_fig=plt_fig, end_effector = e_eff, theta=theta)

    return plt_fig


def getRotationMat(theta):

    # rotation matrix transform for theta
    r_mat = np.array([[np.cos(theta), -1.0*np.sin(theta)],[np.sin(theta), np.cos(theta)]])

    p = np.identity(3)
    p[0:2, 0:2] = r_mat

    return p

def buildConfig(s1, s2, s3, s4):

    r1_rot = getRotationMat(s1)
    r2_rot = getRotationMat(s2)
    r3_rot = getRotationMat(s4)

    rot = [r1_rot, r2_rot, r3_rot]

    new_config = deepcopy(link_config)
    e_eff = deepcopy(end_eff)

    rot_val = np.identity(3)
    z_shift = s3
    origin_x = link_config[0][0]
    for ix,val in enumerate(new_config):

        # update origin from transform of previous link
        new_config[ix][0] = origin_x

        # calculate transform for current link rotation
        n_vec = new_config[ix][1]
        rot_val = np.dot(rot_val, rot[ix])

        # update direction vec
        updated_vec = np.dot(rot_val, np.transpose(n_vec))
        updated_vec = updated_vec/np.linalg.norm(updated_vec)
        #

        if ix == 2:
            e_eff[1] = np.dot(rot_val, np.transpose(e_eff[1]))
        else:
            new_config[ix][1] = updated_vec
            new_config[ix+1][0] = origin_x + updated_vec*new_config[ix][2]
            origin_x = new_config[ix+1][0]

    return new_config, s3, e_eff, s4


def showConfig(s1, s2, s3, s4, fig=None): # [r0, r1, z, r2]

    n_config, z_shift, e_eff, theta = buildConfig(s1, s2, s3, s4)
    fig = plotSkeleton(n_config, z_shift, e_eff, fig=fig, theta = theta )
    return fig

def isWithinReach(x, y, z, theta):

    # ignore reach of theta... assuming range of 0-360
    r_pt = np.r_[x, y]
    abs_dist = np.linalg.norm(r_pt)
    #print(x, y, abs_dist)
    if abs_dist > (l0 + l1) and Z_LIMIT[0] <= z <= Z_LIMIT[1]:
        return False
    else:
        return True


def calculateInverseConfig(x, y, z, theta, fig=None):
    x -= b_pos[0]
    y -= b_pos[1]
    z -= b_pos[2]
    # check if reach is within initial bounds
    if not isWithinReach(x, y, z, theta):
        print("\ngiven point outside workspace, unreachable")
        return None

    # build config for reach
    t_dist = np.linalg.norm(np.r_[x, y])
    # build config for reach
    s1 = (np.math.atan2(-x, y) - np.math.acos((l0 ** 2 + t_dist ** 2 - l1 ** 2) / (2 * l0 * t_dist)))
    s2 = np.pi - np.math.acos((l0 ** 2 + l1 ** 2 - t_dist ** 2) / (2 * l0 * l1))
    s3 = 384 - z
    s4 = theta - s1 - s2

    # check config limits
    if S1_BLIND[0] <= s1 <= S1_BLIND[1] and S2_BLIND[0] <= s2 <= S2_BLIND[1]:
        print("\ngiven point outside workspace, unreachable")
        return None
    #  show & return
    showConfig(s1, s2, s3, s4, fig)
    return [s1, s2, s3, s4]

def resetPosition():

    pass

def resetPosition():
    return

def drawRigidLinks():
    pass

def drawRotationLinks():
    pass
