#!/data/data/com.termux/files/usr/bin/bash

export PACKAGE="TermuxSmsGateway"&&export VERSION="1.0"&&mkdir -p $HOME/.termux/tasks&& \
apt install termux-api git -y&&rm -rf TermuxSmsGateway&& \
git clone https://github.com/deunix-educ/TermuxSmsGateway.git&& \
cp -f $PACKAGE/smsquitto-install/smsquitto-st* $HOME/.termux/tasks/&&cp -f $PACKAGE/smsquitto/smsquitto-conf.yaml $HOME/.termux/&&
cp -f $PACKAGE/smsquitto-install/supervisor/supervisord.conf $PREFIX/etc/ \
cp -f $PACKAGE/smsquitto-install/supervisor/smsquitto.conf $PREFIX/etc/supervisor.d/ \
pip install $PACKAGE/dist/smsquitto-$VERSION.tar.gz \
cd $PREFIX/lib/python3.9/site-packages/supervisor \
patch < $PACKAGE/smsquitto-install/supervisor/patch/http.py.patch \

