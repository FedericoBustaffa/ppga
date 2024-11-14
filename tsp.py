from ppga import algorithms, base, log, tools

toolbox = base.ToolBox()
toolbox.set_weights((-1.0,))

# algorithms.elitist(toolbox, 10)

logger = log.getLogger()
logger.info("ciao")
