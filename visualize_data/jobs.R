genCorr = abs(c(0.17076524068052476, 0.2546180555663148, 0.07498222261861116, 0.2368511770294124, -0.005579682718462679, 0.0190282279225156, 0.0038028483717259943, 0.2588587970296977, 0.00049943902030669, 0.009671553455618126, 0.1549744021970941))
combined = c(1.3300959695953154, 1.5609363641132934, 1.3565194766663784, 1.9680084508058024, 1.5614469228261232, 1.4199985313454895, 1.0828618897787057, 1.6142907296259088, 1.7567347362868382, 1.3406539098362444, 2.2274018190949914)
labelNames = c('people oriented', 'common', 'think', 'important', 'creativity', 'dangerous', 'physical', 'been around', 'glamorous', 'male dominated', 'difficult')
plot(genCorr, combined, main = "jobs",
     xlab = "prob. of generation", ylab = "ease of response")
text(genCorr, combined, labels=labelNames, cex=0.9, font=2)
abline(lm(combined~genCorr), col="red") # regression line (y~x)
