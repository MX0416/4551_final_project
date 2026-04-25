from setuptools import find_packages, setup

package_name = 'gesture_turtlebot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='matt',
    maintainer_email='matthew.xue2004@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'gesture_recognition = gesture_turtlebot.gesture_recognition:main',
            'gesture_to_cmd = gesture_turtlebot.gesture_to_cmd:main',
            'spawn_controller = gesture_turtlebot.spawn_controller:main',  # add this
        ],
    },
)
