import os 

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_prefix

def generate_launch_description():

    # get necessary directory pathes from installed packages
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_scout_gazebo = get_package_share_directory('scout_gazebo')

    # Get whole install dir to avoid having to copy or softlink manually the packages so that gazebo can find them
    description_package_name = "scout_description"
    install_dir = get_package_prefix(description_package_name)

    # Set the path to the WORLD model files. Is to find the models inside the models folder in scout_gazebo package.
    gazebo_models_path = os.path.join(pkg_scout_gazebo, 'models')

    # Gazebo only works with model-related files (meshes and textures), if those files are inside its GAZEBO_MODEL_PATH environment variable
    # Situation for plugin-related files is the same (GAZEBO_PLUGIN_PATH)
    # Apend path of our model files and the path of our install dir into GAZEBO_MODEL_PATH if its exists (otherwise create it)
    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] =  os.environ['GAZEBO_MODEL_PATH'] + ':' + install_dir + '/share' + ':' + gazebo_models_path
    else:
        os.environ['GAZEBO_MODEL_PATH'] =  install_dir + "/share" + ':' + gazebo_models_path

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = os.environ['GAZEBO_PLUGIN_PATH'] + ':' + install_dir + '/lib'
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'


    print("GAZEBO MODELS PATH=="+str(os.environ["GAZEBO_MODEL_PATH"]))
    print("GAZEBO PLUGINS PATH=="+str(os.environ["GAZEBO_PLUGIN_PATH"]))


    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        )
    )    

    return LaunchDescription([
        DeclareLaunchArgument(
          'world',
          default_value=[os.path.join(pkg_scout_gazebo, 'worlds', 'smalltown.world'), ''],
          description='SDF world file'),
          
        gazebo
    ])
