if [ $# -ne 1 ]; then
    echo 'You need to input first argument as waiting time for each step.'

    exit 1
fi


while true
do
    python CDEFGABCn.py -f ./musics/twinkle_twinkle_little_star.m
    sleep ${1}s

    python CDEFGABCn.py -f ./musics/ode_to_joy.m
    sleep ${1}s

    python CDEFGABCn.py -f ./musics/when_the_saints_go_marching_in.m
    sleep ${1}s

    python CDEFGABCn.py -f ./musics/joy_to_the_world.m
    sleep ${1}s
done
