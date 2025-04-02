from m1n1.trace.admac import ADMACTracer

admac_tracer = ADMACTracer(hv, "/arm-io/admac-aop-audio", verbose=3)
admac_tracer.start()
hv.trace_irq('/arm-io/admac-aop-audio', 600, 1, hv.IRQTRACE_IRQ)

#admac_tracer2 = ADMACTracer(hv, "/arm-io/admac-sio", verbose=3)
#admac_tracer2.start()
#hv.trace_irq('/arm-io/admac-sio', 1118, 1, hv.IRQTRACE_IRQ)
