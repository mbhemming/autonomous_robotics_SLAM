class KalmanFilter():

    R_MotionVariance = 0.05
    Q_MeasurementVariance = 1.5

    A = 1
    B = 0
    C = 1

    CovX = 0.05
    CovY = 0.05

    
    def InitKalman(self, initX, initY):
        self.stateEstimateX = initX
        self.stateEstimateY = initY
        
    def DoUpdateX ( self, measuredX ):
        
        #state estimate of X maintained using odometry 
        #for the motion model
        
        _CovX = A*CovX*A + R_MotionVariance
        
        KGain = _CovX * C * ((C*CovX*C + Q_MeasurementVariance)**(-1))
        
        self.x = self.x + KGain(measuredX - C*self.x)
        
        CovX = (1 - KGain*C)*CovX
        
        
    def DoUpdateY ( self, measuredX ):
        
        #state estimate of X maintained using odometry 
        #for the motion model
        
        _CovY = A*CovY*A + R_MotionVariance
        
        KGain = _CovY * C * ((C*CovY*C + Q_MeasurementVariance)**(-1))
        
        self.y = self.y + KGain(measuredY - C*self.y)
        
        CovY = (1 - KGain*C)*CovY
                

