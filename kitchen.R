genCorr = abs(c(0.5323111426150905, 0.45066043215834845, 0.5310725900811576, 0.48771763519993, 0.5094253391194362, 0.10255125976511446, -0.14225560857539987, 0.013828408304296968, 0.17403243707330637, 0.2665930694697609, 0.23928122712203087))
combined = c(2.1336138143507486, 1.5806180081304801, 1.5245264425652085, 1.7177768916119387, 1.3948471200836197, 1.1420218319492679, 0.8029263040483713, 1.1528151633015107, 2.15341392351095, 2.037698047498753, 0.7579103860316669)
labelNames = c('common', 'essential', 'plain sight', 'often', 'think', 'dangerous', 'loud', 'metallic', 'expensive', 'easy', 'heavy')
plot(genCorr, combined, main = "kitchen appliances",
     xlab = "prob. of generation", ylab = "ease of response")
text(genCorr, combined, labels=labelNames, cex=0.9, font=2)
abline(lm(combined~genCorr), col="red") # regression line (y~x)

