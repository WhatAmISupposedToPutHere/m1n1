import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import struct
from construct import *

from m1n1.setup import *
from m1n1.hw.dart import DART
from m1n1.fw.aop.client import AOPClient
from m1n1.fw.aop.ipc import *

# aop nodes have no clocks described in adt for j293. it does it itself
p.pmgr_adt_clocks_enable("/arm-io/aop")
p.pmgr_adt_clocks_enable("/arm-io/dart-aop")

dart = DART.from_adt(u, "/arm-io/dart-aop",
                     iova_range=(u.adt["/arm-io/dart-aop"].vm_base, 0x1000000000))
dart.initialize()

aop = AOPClient(u, "/arm-io/aop", dart)
aop.update_bootargs({
    'p0CE': 0x20000,
    'laCn': 0x0,
#    'tPOA': 0x1,
    "gila": 0x40,
})
aop.verbose = 4

p.dapf_init_all()
aop.asc.OUTBOX_CTRL.val = 0x20001 # (FIFOCNT=0x0, OVERFLOW=0, EMPTY=1, FULL=0, RPTR=0x0, WPTR=0x0, ENABLE=1)

aop.start()
for epno in [0x20, 0x21, 0x23, 0x22, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x2b]:
    aop.start_ep(epno)

aop.work_for(3)
alsep = aop.als
alsep.VERBOSE = True
ret = alsep.send_notify(ALSSetPropertyVerbosity(level=6))
ret = alsep.send_notify(ALSSetPropertyCalibration(value=b'\x01\x02\x00\x00\x00\x00\x00\x00\x00\x01\xc1\x00\x9aY\xfa\x00d\x00c\x00>\x00\x06\x06\x06\x06\x05\x05\xb8\xdc4\xbaP\xc8`;^-\xd4<\xef\xc0\x15=\x1a\xec\x91<\x1cN\xabF&\x1a\x03\xc5\xca\xf9\xacE\x8c$\xa2\xc5.\x0f\x1cE\x02\x00\x00\x00\x00)\x00\x00\x80\x00\x80\x00\x80\x00\x80\x9e\x7f\xb9\x7f1\x80\xe1\x7f\xd0\x7f\x06\x00\x00\x00\x00\x15\x00\x00\x80\x00\x80\x00\x80\x00\x80\xb0\x7f\xb0\x7f\x00\x80\xc1\x7f\xce\x7f\x07\x00\x00\x00\x00%\x00\x00\x80\x00\x80\x00\x80\x00\x80\x91\x7f\x9c\x7f\t\x80\xb4\x7f\x87\x7f\x05\x00\x00\x00\x00\x1b\x00\x00\x80\x00\x80\x00\x80\x00\x80\x98\x7f\xaa\x7f\x1e\x80\xfa\x7f\n\x80\x06\x00\x00\x00\x00\x17\x00\x00\x80\x00\x80\x00\x80\x00\x80\x9e\x7f\xb4\x7f\x1b\x80\xf8\x7f*\x80'))
ret = alsep.send_notify(ALSSetPropertyInterval(interval=200000))
aop.work_for(60)
