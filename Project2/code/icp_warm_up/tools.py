import numpy as np
import transforms3d as t3d

from scipy.spatial import KDTree
from tqdm import tqdm

def sync_time_stamps(t1, t2):
    t1_synced = []
    ind = 0
    for i in range(len(t1)):
        while(t2[ind] < t1[i] and ind < len(t2) - 1):
            ind += 1
        t1_synced.append(ind)
    return np.array(t1_synced)


def Kabsch(m, z):
    # Kabsch algorithm
    # From m to z
    # z: source point cloud
    # m: target point cloud

    z_bar = np.mean(z, axis=0)
    m_bar = np.mean(m, axis=0)

    delta_z = (z - z_bar).reshape(len(z), 3, 1)
    delta_m = (m - m_bar).reshape(len(m), 3, 1)

    Q = np.zeros((3, 3))
    for i in range(len(z)):
        mult = delta_m[i] @ delta_z[i].T
        Q += mult

    # SVD
    U, s, Vt = np.linalg.svd(Q)
    det_UV = np.linalg.det(U @ Vt)
    mid_matrix = np.eye(3)
    mid_matrix[2][2] = det_UV

    R = U @ mid_matrix @ Vt
    p = m_bar - R @ z_bar

    return R, p


def ICP(z, m, R_0=None, p_0=None, iter=70, init_guesses=15, max_yaw=30):
    # ICP algorithm
    # z: source point cloud
    # m: target point cloud
    # Transforming z into m
    # i.e. finding the transformation from m to z
    z = np.array(z)
    m = np.array(m)

    best_R, best_p = np.eye(3), np.zeros(3)

    yaw_angles = np.linspace(-max_yaw, max_yaw, init_guesses)
    min_err = np.inf

    if R_0 is not None:
        m_hat = (R_0 @ z.T).T + p_0
        z_assoc = np.zeros_like(m)

        for _ in range(70):
            # Associate points
            tree = KDTree(m_hat)
            dist, idx = tree.query(m)
            z_assoc = z[idx]

            R, p = Kabsch(m, z_assoc)

            p = p.reshape(3)
            m_hat = (R @ z.T).T + p

            m_temp = (R @ z_assoc.T).T + p
            err = np.sum(np.linalg.norm(m - m_temp, axis=1))

            if err < min_err:
                min_err = err
                best_R = R
                best_p = p

    for yaw in yaw_angles:
        R_0 = t3d.euler.euler2mat(0, np.radians(yaw), np.radians(yaw))
        p_0 = np.mean(m, axis=0) - np.mean(z, axis=0)

        m_hat = (R_0 @ z.T).T + p_0
        z_assoc = np.zeros_like(m)

        for _ in range(iter):
            # Associate points
            tree = KDTree(m_hat)
            dist, idx = tree.query(m)
            z_assoc = z[idx]

            R, p = Kabsch(m, z_assoc)

            p = p.reshape(3)
            m_hat = (R @ z.T).T + p

            m_temp = (R @ z_assoc.T).T + p
            err = np.sum(np.linalg.norm(m - m_temp, axis=1))

            if err < min_err:
                min_err = err
                best_R = R
                best_p = p

    return best_R, best_p