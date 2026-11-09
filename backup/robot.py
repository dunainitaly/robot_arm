import numpy as np

from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

L1 = 100
L2 = 95
L3 = 128

robot = Chain(
    name="merkur_beta_6",
    links=[
        OriginLink(),

        URDFLink(
            name="base",
            origin_translation=[0, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 1, 0],
            bounds=(-np.pi, np.pi),
        ),

        URDFLink(
            name="shoulder",
            origin_translation=[0, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 0, 1],
            bounds=(-np.pi/2, np.pi/2),
        ),

        URDFLink(
            name="elbow",
            origin_translation=[L1, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 0, 1],
            bounds=(-np.pi/2, np.pi/2),
        ),

        URDFLink(
            name="wrist",
            origin_translation=[L2, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 0, 1],
            bounds=(-np.pi/2, np.pi/2),
        ),

        URDFLink(
            name="pen",
            origin_translation=[L3, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=None,
            joint_type="fixed",
        ),
    ],
    active_links_mask=[False, True, True, True, True, False],
)
