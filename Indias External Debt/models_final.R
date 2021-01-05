library("tseries")
library("TTR")
library("fUnitRoots")
library("lmtest")
library("forecast")
library("ggplot2")

debt=read.csv("C:\\Users\\jyoth\\OneDrive\\Desktop\\Ext Debt\\External Debt.csv")
nrow(debt)
names(debt)

#========================================================MULTILATERAL===============================================
multilat <- debt["I..Total.Multilateral"]
multilat <- ts(multilat,start = 1991,end = 2019,frequency = 1 )
multilat_train <- window(multilat, start=1991, end=2015)
multilat_test <- window(multilat, start=2016, end=2019)
plot.ts(multilat)

#TEST FOR STATIONARITY
adf.test(multilat_train, alternative = "stationary")

multilat_stat = diff(multilat_train, differences=2)   #Multilateral made stationary
adf.test(multilat_stat, alternative = "stationary")
plot(multilat_stat)

acf(multilat, lag.max=34)
pacf(multilat, lag.max=34)

#ARIMA
mult <- auto.arima(multilat_train, approximation = FALSE, max.order = 10 )
mult
tsdisplay(residuals(mult), lag.max=45, main='(0,1,0) Model Residuals') 
fcast_mult <- forecast(mult, h=5)

#Accuracy check
plot(fcast_mult, main=" ")
lines(multilat_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red", "blue"),c("Actual","Predicted"))
accuracy(fcast_mult,multilat_test)

#===================================================BILATERAL(4)=====================================================
bilat <- debt["II.Total.Bilateral"]
bilat <- ts(bilat,start = 1991,end = 2019,frequency = 1 )
bilat_train <- window(bilat, start=1991, end=2015)
bilat_test <- window(bilat, start=2016, end=2019)
plot.ts(bilat)

#TEST FOR STATIONARITY
adf.test(bilat_train, alternative = "stationary")
bilat_stat = diff(bilat, differences=2)  
adf.test(bilat_stat, alternative = "stationary")
plot(bilat_stat)

acf(bilat_stat, lag.max=34)
pacf(bilat_stat, lag.max=34)

# lambda <- BoxCox.lambda(bilat, method=c("guerrero"))
# lambda
# x.transform <- BoxCox(x,lambda)
# plot(x.transform)

#4 - NNETAR  - THISSSSS
nnetar_bi <- nnetar(bilat_train,size=5)
fcast_bi <- forecast(nnetar_bi, h=5)

#Accuracy Check
plot(fcast_bi, main=" ")
lines(bilat_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_bi,bilat_test)


#=================================================???IMF(1 or 4)=====================================================
imf <- debt["III..International.Monetary.Fund"]
imf <- ts(imf,start = 1991,end = 2019,frequency = 1 )
imf_train <- window(imf, start=1991, end=2015)
imf_test <- window(imf, start=2016, end=2019)
plot.ts(imf)

#TEST FOR STATIONARITY
adf.test(imf, alternative = "stationary")
imf_stat = diff(imf, differences=2)  
adf.test(imf_stat, alternative = "stationary")
plot(imf_stat)

acf(imf_stat, lag.max=34)
pacf(imf_stat, lag.max=34)

#1 - Better?
imf_ARIMA <- arima(imf_train, order=c(0,2,1),method="ML")    #OR (0,2,1) (5,2,0)
coeftest(imf_ARIMA)
fcast_imf <- forecast(imf_ARIMA, h=5)

#4 - NNETAR
nnetar_imf <- nnetar(imf_train,size=5)
fcast_imf <- forecast(nnetar_imf, h=5)

#Accuracy Check
plot(fcast_imf, main=" ")
lines(imf_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_imf,imf_test)

#=====================================================TTC=========================================================
ttc <- debt["IV.Total.Trade.Credit"]
ttc <- ts(ttc,start = 1991,end = 2019,frequency = 1 )
ttc_train <- window(ttc, start=1991, end=2015)
ttc_test <- window(ttc, start=2016, end=2019)
plot.ts(ttc)

#TEST FOR STATIONARITY
adf.test(ttc_train, alternative = "stationary")
ttc_stat = diff(ttc_train, differences=3)   #Multilateral made stationary
adf.test(ttc_stat, alternative = "stationary")
plot(ttc_stat)

#2 - BESHT
model_ttc <- auto.arima(ttc_train, seasonal = FALSE, approximation = FALSE)
model_ttc
tsdisplay(residuals(model_ttc), lag.max=45, main='(1,1,0) Model Residuals') 
fcast_ttc <- forecast(model_ttc, h=5)

#Accuracy Check
plot(fcast_ttc, main=" ")
lines(ttc_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_ttc,ttc_test)

#=======================================================TCB==========================================================
tcb <- debt["V.Total.Commercial.Borrowing"]
tcb <- ts(tcb,start = 1991,end = 2019,frequency = 1 )
tcb_train <- window(tcb, start=1991, end=2015)
tcb_test <- window(tcb, start=2016, end=2019)
plot.ts(tcb)

#TEST FOR STATIONARITY
adf.test(tcb_train, alternative = "stationary")
tcb_stat = diff(tcb, differences=2)   #Multilateral made stationary
adf.test(tcb_stat, alternative = "stationary")
plot(tcb_stat)

acf(tcb_stat, lag.max=34)
pacf(tcb_stat, lag.max=34)

#Model
model_tcb <- auto.arima(tcb_train, seasonal = FALSE, approximation = FALSE)
model_tcb
tsdisplay(residuals(model_tcb), lag.max=45, main='(0,2,1) Model Residuals') 
fcast_tcb <- forecast(model_tcb, h=5)

#Accuracy Check
plot(fcast_tcb, main=" ")
lines(tcb_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_tcb,tcb_test)


#======================================================NRI===========================================================
nri <- debt["VI..NRI...FC.B.O..Deposits"]
nri<-  ts(nri,start = 1991,end = 2019,frequency = 1 )
nri_train <- window(nri, start=1991, end=2015)
nri_test <- window(nri, start=2016, end=2019)
plot.ts(nri)

#TEST FOR STATIONARITY
adf.test(nri_train, alternative = "stationary")
nri_stat = diff(nri_train, differences=3) 
adf.test(nri_stat, alternative = "stationary")
plot(nri_stat)

acf(nri_stat, lag.max=34)
pacf(nri_stat, lag.max=34)

#ARIMA
nri_ARIMA <- arima(nri_train, order=c(0,3,1),method="ML")  
coeftest(nri_ARIMA)
fcast_nri <- forecast(nri_ARIMA, h=5)

#Accuracy Check
plot(fcast_nri, main=" ")
lines(nri_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_nri,nri_test)


#====================================================Rs==============================================================
rs <- debt["VII..Total.Rupee.Debt"]
rs<-  ts(rs,start = 1991,end = 2019,frequency = 1 )
rs_train <- window(rs, start=1991, end=2015)
rs_test <- window(rs, start=2016, end=2019)
plot.ts(rs)

#TEST FOR STATIONARITY
adf.test(rs_train, alternative = "stationary")
rs_stat = diff(rs, differences=2)   #Multilateral made stationary
adf.test(rs_stat, alternative = "stationary")
plot(rs_stat)

acf(rs_stat, lag.max=34)
pacf(rs_stat, lag.max=34)

#Model
model_rs <- auto.arima(rs_train, seasonal = FALSE, approximation = FALSE)
tsdisplay(residuals(model_rs), lag.max=45, main='(0,2,1) Model Residuals') 
fcast_rs <- forecast(model_rs, h=5)

#Accuracy Check
plot(fcast_rs, main=" ")
lines(rs_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_rs,rs_test)

#===================================================LTD==============================================================
ltd<- debt["VIII..Total.Long.Term.Debt"]
ltd<-  ts(ltd,start = 1991,end = 2019,frequency = 1 )
ltd_train <- window(ltd, start=1991, end=2015)
ltd_test <- window(ltd, start=2016, end=2019)
plot.ts(ltd)

#TEST FOR STATIONARITY
adf.test(ltd_train, alternative = "stationary")
ltd_stat = diff(ltd_train, differences=2)   
adf.test(ltd_stat, alternative = "stationary")
plot(ltd_stat)

acf(ltd_stat, lag.max=34)
pacf(ltd_stat, lag.max=34)

#NNETAR Model
nnetar_ltd <- nnetar(ltd_train,size=5)
fcast_ltd <- forecast(nnetar_ltd, h=4)

#Accuracy Check
plot(fcast_ltd, main="Long Term Debt")
lines(ltd_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_ltd,ltd_test)


#Prediction 
pred_ltd <- forecast(nnetar_ltd, h=10)
pred_ltd <- ts(pred_ltd$mean[5:15], start=2020, end=2025)
# plot(final, main ="Long Term Debt", col="blue")
# lines(pred_ltd, col="red")
# legend("topleft",lty=1,bty = "n",col=c("blue","red"),c("Actual","Predicted"))
# typeof(ltd)
seqplot.ts(ltd,pred_ltd,colx = "blue", coly = "red", size=2,pchy = 2, main="Long Term Debt", xlab="Years", ylab="Debt Amount (in USD milions)")
legend("topleft",lty=1,bty = "n",col=c("blue","red"),c("Actual","Predicted"))
plot.ts(final)

# names <- c(rep("Actual",29),rep("Predicted",6))  #used for all ggplots
years<- c(time(ltd), time(pred_ltd))      #Used for all ggplots

final<- ts.union(ltd,pred_ltd)
final<-data.frame(years,final)
colnames(final) <- c("years", "ltd", "pred_ltd")
ggplot(final, aes(x=years, y=c(ltd,pred_ltd)))+
  geom_line(aes(x=years,y=ltd), linetype="solid",color="blue",size=2) +
  geom_line(aes(x=years,y=pred_ltd), linetype="solid",color="red",size=2) +
  labs(x="Years",y="Debt Amount (in USD milions)",title="Long Term Debt") +
  # legend("topleft",lty=1,bty = "n",col=c("blue","red"),c("Actual","Predicted"))  #+
  theme(plot.title = element_text(hjust = 0.5, face = "bold", size=20))

#=====================================================STD============================================================
std<- debt["IX..Total.Short.term.Debt"]
std<-  ts(std,start = 1991,end = 2019,frequency = 1 )
std_train <- window(std, start=1991, end=2015)
std_test <- window(std, start=2016, end=2019)
plot.ts(std)

#TEST FOR STATIONARITY
adf.test(std_train, alternative = "stationary")
std_stat = diff(std_train, differences=3) 
adf.test(std_stat, alternative = "stationary")
plot(std_stat)

acf(std_stat, lag.max=34)
pacf(std_stat, lag.max=34)

#2 - THIS
model_std <- auto.arima(std_train, seasonal = FALSE, approximation = FALSE)
model_std
tsdisplay(residuals(model_std), lag.max=45, main='(0,2,1) Model Residuals') 
fcast_std <- forecast(model_std, h=4)
# model_std <- auto.arima(std, seasonal = FALSE, approximation = FALSE)

#Accuracy Check
plot(fcast_std, main="Short Term Debt")
lines(std_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_std,std_test)

#Prediction 
pred_std <- forecast(model_std, h=10)
pred_std <- ts(pred_std$mean[5:10], start=2020, end=2025)

seqplot.ts(std,pred_std,colx = "blue", coly = "red", main="Short Term Debt", xlab="Years", ylab="Debt Amount (in USD milions)")
legend("topleft",lty=1,bty = "n",col=c("blue","red"),c("Actual","Predicted"))

final<- ts.union(std,pred_std)
final<-data.frame(years,final)
colnames(final) <- c("years", "std", "pred_std")
ggplot(final, aes(x=years, y=c(std,pred_std)))+
  geom_line(aes(x=years,y=std), linetype="solid",color="blue",size=2) +
  geom_line(aes(x=years,y=pred_std), linetype="solid",color="red",size=2) +
  labs(x="Years",y="Debt Amount (in USD milions)",title="Short Term Debt") +
  theme(plot.title = element_text(hjust = 0.5, face = "bold", size=20)) + 
  

#==================================================Total Debt=========================================================

total_debt <- debt["Gross.Total.Debt"]
total_debt <- ts(total_debt,start = 1991,end = 2019,frequency = 1 )
debt_train <- window(total_debt, start=1991, end=2015)
debt_test <- window(total_debt, start=2016, end=2019)
plot.ts(total_debt)

#TEST FOR STATIONARITY
adf.test(debt_train, alternative = "stationary")
debt_stat = diff(debt_train, differences=3)   #Multilateral made stationary
adf.test(debt_stat, alternative = "stationary")
plot(debt_stat)

acf(debt_stat, lag.max=34)
pacf(debt_stat, lag.max=34)

#1 - ARIMA
debt_ARIMA <- arima(debt_train, order=c(2,3,0),method="ML")
coeftest(debt_ARIMA)
fcast_debt <- forecast(debt_ARIMA, h=4)
debt_ARIMA <- arima(total_debt, order=c(2,3,0),method="ML")

#Accuracy Check
plot(fcast_debt, main="Gross Total Debt")
lines(debt_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_debt,debt_test)

#Prediction 
pred_debt <- forecast(debt_ARIMA, h=6)
pred_debt <- ts(pred_debt$mean, start=2020, end=2025)
seqplot.ts(total_debt,pred_debt,colx = "blue", coly = "red", main="Gross Total Debt", xlab="Years", ylab="Debt Amount (in USD milions)")
legend("topleft",lty=1,bty = "n",col=c("blue","red"),c("Actual","Predicted"))

years<- c(time(ltd), time(pred_ltd))
final<- ts.union(total_debt,pred_debt)
final<-data.frame(years,final)
colnames(final) <- c("years", "total_debt","pred_debt")
ggplot(final, aes(x=years, y=c(total_debt,pred_debt)))+
  geom_line(aes(x=years,y=total_debt), linetype="solid",color="blue",size=2) +
  geom_line(aes(x=years,y=pred_debt), linetype="solid",color="red",size=2) +
  labs(x="Years",y="Debt Amount (in USD milions)",title="Gross Total Debt") +
  theme(plot.title = element_text(hjust = 0.5, face = "bold", size=20))


#=============================================================DSR=============================================================
service_ratio <- debt["Debt.Service.Ratio..."]
service_ratio <- ts(service_ratio,start = 1991,end = 2019,frequency = 1 )
service_train <- window(service_ratio, start=1991, end=2015)
service_test <- window(service_ratio, start=2016, end=2019)
plot.ts(service_ratio)

#TEST FOR STATIONARITY
adf.test(service_train, alternative = "stationary")
service_stat = diff(service_train, differences=2)   #Multilateral made stationary
adf.test(service_stat, alternative = "stationary")
plot(service_stat)

acf(service_stat, lag.max=34)
pacf(service_stat, lag.max=34)

#1 - ARIMA
service_ARIMA <- arima(service_train, order=c(1,2,1),method="ML")
coeftest(service_ARIMA)
fcast_service <- forecast(service_ARIMA, h=4)
# service_ARIMA <- arima(service_ratio, order=c(1,2,1),method="ML")

#Accuracy Check
plot(fcast_service, main="Debt Service Ratio")
lines(service_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_service,service_test)

#Prediction 
pred_service <- forecast(service_ARIMA, h=10)
pred_service <- ts(pred_service$mean[5:10], start=2020, end=2025)
seqplot.ts(service_ratio,pred_service,colx = "blue", coly = "red", main="Debt Service Ratio (DSR)", xlab="Years", ylab="DSR (in %)")
legend("topright",lty=1,bty = "n",col=c("blue","red"),c("Actual","Predicted"))

final<- ts.union(service_ratio,pred_service)
final<-data.frame(years,final)
colnames(final) <- c("years", "service_ratio","pred_service")
ggplot(final, aes(x=years, y=c(service_ratio,pred_service)))+
  geom_line(aes(x=years,y=service_ratio), linetype="solid",color="blue",size=2) +
  geom_line(aes(x=years,y=pred_service), linetype="solid",color="red",size=2) +
  labs(x="Years",y="DSR (in %)",title="Debt Service Ratio (DSR)") +
  theme(plot.title = element_text(hjust = 0.5, face = "bold", size=20))

#========================================================DGDP=======================================================

DGDP <- debt["Debt.Stock...GDP.Ratio"]
DGDP <- ts(DGDP,start = 1991,end = 2019,frequency = 1 )
DGDP_train <- window(DGDP, start=1991, end=2015)
DGDP_test <- window(DGDP, start=2016, end=2019)
plot.ts(DGDP)

#TEST FOR STATIONARITY
adf.test(DGDP_train, alternative = "stationary")
DGDP_stat = diff(DGDP_train, differences=1)   #Multilateral made stationary
adf.test(DGDP_stat, alternative = "stationary")
plot(DGDP_stat)

acf(DGDP_stat, lag.max=34)
pacf(DGDP_stat, lag.max=34)

#NNETAR
# nnetar_DGDP <- nnetar(DGDP_train,size=5)
fcast_DGDP <- forecast(nnetar_DGDP, h=4)
nnetar_DGDP <- nnetar(DGDP,size=5)

#Accuracy Check
plot(fcast_DGDP, main="Debt to GDP Ratio")
lines(DGDP_test, col="red")
legend("topleft",lty=1,bty = "n",col=c("red","blue"),c("Actual","Predicted"))
accuracy(fcast_DGDP,DGDP_test)

#Prediction 
pred_DGDP <- forecast(nnetar_DGDP, h=6)
pred_DGDP <- ts(pred_DGDP$mean, start=2020, end=2025)
#LABELLSSSSSS
seqplot.ts(DGDP,pred_DGDP,colx = "blue", coly = "red", 
           main="Debt Stock to GDP Ratio", xlab="Years", ylab="Debt Stock to GDP Ratio (in %)")
legend("topright",lty=1,bty = "n",col=c("blue","red"),c("Actual","Predicted"))

final<- ts.union(DGDP,pred_DGDP)
final<-data.frame(years,final)
colnames(final) <- c("years","DGDP", "pred_DGDP")
ggplot(final, aes(x=years, y=c(DGDP,pred_DGDP)))+
  geom_line(aes(x=years,y=DGDP), linetype="solid",color="blue",size=2) +
  geom_line(aes(x=years,y=pred_DGDP), linetype="solid",color="red",size=2) +
  labs(x="Years",y="Debt Stock to GDP Ratio (in %)",title="Debt Stock to GDP Ratio") +
  theme(plot.title = element_text(hjust = 0.5, face = "bold", size=20))
