genCorr = abs(c(-0.016752173733000794, -0.03950684312667569, 0.09511255394503539, -0.17428491077383237, 0.18083577002258705, 0.5359626511977721, 0.5845506051005428, 0.5506060109052386, 0.4159679097116104, 0.4987269939170238))
combined = c(1.0148157841852952, 0.6815335632538537, 0.8813111155593616, 0.5143986164416299, 1.2079916046585866, 1.334540064277405, 1.142627128919521, 1.1502194194748625, 0.6816802157601393, 1.2200114841288323)
labelNames = c('reflective', 'early', 'partying', 'political', 'meaningful', 'time off', 'think', 'likes', 'romantic', 'widely celebrated')
plot(genCorr, combined, main = "sports",
     xlab = "prob. of generation", ylab = "ease of response")
text(genCorr, combined, labels=labelNames, cex=0.9, font=2)
abline(lm(combined~genCorr), col="red") # regression line (y~x)
