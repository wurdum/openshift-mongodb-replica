instances=(m1 m2 m3)

for i in ${instances[@]}; do
    if [ "$i" = "$1" ]; then
        rm -rf /srv/$1/.openshift
        rm -rf /srv/$1/*
        cp -r /srv/mongo-replica-config/* /srv/$1/
        cp -r /srv/mongo-replica-config/.openshift /srv/$1/
        cd /srv/$1
        git add .
        git commit -am "$1"
        git push origin

        echo "updating $1 is done"
        exit 0
    fi
done

echo "$1 instance not found"