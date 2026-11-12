        plane = Plane(point=[0, 0, 0], normal=[0, 0, 1])
        points = project_to_plane(
            plane=plane,
            points=Points(points)
        )

        frames = points_to_frames(points, np.array([
            [ 0, 0,  1],
            [ 0, 1,  0],
            [-1, 0,  0],
        ]))

        print(frames)
        points =  np.asarray(points)
        trajectory = robot.inverse_kinematics_trajectory_frame(
            frames,
            initial_position=current_joints,
            orientation_mode="all",
            regularization_parameter=0.01
        )
        # print(trajectory)


        for frame, joints in zip(frames, trajectory):
            print(robot.forward_kinematics(joints))


        visualise(points)
