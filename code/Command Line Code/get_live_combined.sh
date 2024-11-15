a=$(cat tf\ data)

frame_id='unkown'
x=''
y=''
zFacing=''
time=''

x_Found="False"
y_Found="False"

while IFS= read -r line
do
    line_no_lead_space="$(echo -e "${line}" | sed -e 's/^[[:space:]]*//')"
    first_2_chars=${line_no_lead_space:0:2}

    if [ $first_2_chars = 'fr' ]; then
        frame_id=$(cut -c 11- <<<"$line_no_lead_space")
        x_Found="False"
        y_Found="False"

    fi

    if [ "$first_2_chars" = "x:" ]; then
        if [ "$x_Found" = "False" ]; then
            x=$(cut -c 4- <<<"$line_no_lead_space")
            x_Found="True"
        fi
    fi
    if [ "$first_2_chars" = "y:" ]; then
        if [ "$y_Found" = "False" ]; then
            y=$(cut -c 4- <<<"$line_no_lead_space")
            y_Found="True"
        fi
    fi
    if [ "$first_2_chars" = "z:" ]; then
        zFacing=$(cut -c 4- <<<"$line_no_lead_space")
    fi
    if [ "$first_2_chars" = "se" ]; then
        seconds=$(cut -c 7- <<<"$line_no_lead_space")
    fi

    all_data="${x},${y},${zFacing},${seconds},${frame_id}"

    if [ $frame_id = '"odom_combined"' ]; then
        if [ "$first_2_chars" = "tf" ]; then
            echo $all_data
        fi
    fi
        
done <<< "$a"
