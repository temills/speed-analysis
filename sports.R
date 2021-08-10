genCorr = abs(c(0.5411744845692085, 0.5814709969892956, 0.6487580074053295, 0.45308748027122253, 0.30486850156710427, 0.0889992003601851, -0.024276796370763777, 0.17906979519434446, 0.012709898648517461, 0.2568288124641362))
combined = c(1.3422595319016208, 2.4740060823847245, 2.3106646812348566, 2.715881148693045, 1.886396087543236, 1.1455198115314706, 1.2712206236136547, 1.968625039902069, 1.2778090594208569, 1.2186310236281495)
labelNames = c('think', 'popular', 'spectators', 'competitive', 'strenuous', 'dangerous', 'expensive', 'been around', 'flexibility', 'learn')
plot(genCorr, combined, main = "sports",
     xlab = "prob. of generation", ylab = "ease of response")
text(genCorr, combined, labels=labelNames, cex=0.9, font=2)
abline(lm(combined~genCorr), col="red") # regression line (y~x)


