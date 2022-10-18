import numpy as np

class Interp1D():
    def __init__(self,xeval=None,xint=None,yint=None,yprimeint=None,N=None,f=None,Neval=None,a=None,b=None,Nint=None):
        '''
        xeval = one point we want to evaluate at
        xint = interp nodes
        yint = f(interp nodes)
        yprimeint = f'(interp nodes)
        N = degree of our polynomial
        '''
        self.xeval = xeval
        self.xint = xint
        self.yint = yint
        self.yprimeint = yprimeint
        self.N = N
    def lagrange(self,xeval=None,xint=None,yint=None,N=None):
        # Verify that needed vars are inputted somewhere
        if xeval is None:
            if self.xeval is None:
                raise ValueError("Please input xeval")
            else:
                xeval = self.xeval
        if xint is None:
            if self.xint is None:
                raise ValueError("Please input xint")
            else:
                xint = self.xint
        if yint is None:
            if self.yint is None:
                raise ValueError("Please input yint")
            else:
                yint = self.yint
        if N is None:
            if self.N is None:
                raise ValueError("Please input N")
            else:
                N = self.N
        
        lj = np.ones(N+1)
        
        for count in range(N+1):
            for jj in range(N+1):
                if (jj != count):
                    lj[count] = lj[count]*(xeval - xint[jj])/(xint[count]-xint[jj])

        yeval = 0.
        
        for jj in range(N+1):
            yeval = yeval + yint[jj]*lj[jj]

        return(yeval)
    def eval_barycentric(self, xeval=None,xint=None,yint=None):
        # Verify that needed vars are inputted somewhere
        if xeval is None:
            if self.xeval is None:
                raise ValueError("Please input xeval")
            else:
                xeval = self.xeval
        if xint is None:
            if self.xint is None:
                raise ValueError("Please input xint")
            else:
                xint = self.xint
        if yint is None:
            if self.yint is None:
                raise ValueError("Please input yint")
            else:
                yint = self.yint
        
        phi = np.prod(np.array([(xeval - i) for i in xint]))
        total_sum = 0

        for idx, xj in enumerate(xint):
            wj = np.prod(np.array([(1/(xj - xi)) for xi in xint if xi != xj]))
            fxj = yint[idx]
            total_sum += (wj / (xeval - xj))*fxj

        return phi*total_sum
    def hermite(self,xeval=None,xint=None,yint=None,yprimeint=None):
        # Verify that needed vars are inputted somewhere
        if xeval is None:
            if self.xeval is None:
                raise ValueError("Please input xeval")
            else:
                xeval = self.xeval
        if xint is None:
            if self.xint is None:
                raise ValueError("Please input xint")
            else:
                xint = self.xint
        if yint is None:
            if self.yint is None:
                raise ValueError("Please input yint")
            else:
                yint = self.yint
        if yprimeint is None:
            if self.yprimeint is None:
                raise ValueError("Please input yprimeint")
            else:
                yprimeint = self.yprimeint

        px = 0
        # Below for loop handles both sums
        for idx, xj in enumerate(xint):
            # Calculate l_j^2(xj)
            lj = np.prod(np.array([(xeval - xi)/(xj - xi) for jdx, xi in enumerate(xint) if idx != jdx]))
            lj_squared = lj**2

            # Calculate q_j(x)
            lprime_j = np.prod(np.array([(xj - xi) for jdx, xi in enumerate(xint) if idx != jdx]))
            qjx = (1 - 2*(xeval - xj)*lprime_j)*lj_squared

            # Calculate r_j(x)
            rjx = (xeval - xj)*lj_squared

            # Add to the interpolation evaluation
            px += (yint[idx]*qjx + yprimeint[idx]*rjx)
        
        return px
    def linear_spline(self,xeval=None,xint=None,yint=None):
        # Verify that needed vars are inputted somewhere
        if xeval is None:
            if self.xeval is None:
                raise ValueError("Please input xeval")
            else:
                xeval = self.xeval
        if xint is None:
            if self.xint is None:
                raise ValueError("Please input xint")
            else:
                xint = self.xint
        if yint is None:
            if self.yint is None:
                raise ValueError("Please input yint")
            else:
                yint = self.yint

        def find_points(xeval, xint, idx):
            """
            xeval is the larger array of points
            xint is the smaller array of intervals
            idx is the interval index (counting from 1)
            """
            indices = np.where(np.logical_and(xeval <= xint[idx+1], xeval >= xint[idx]))[0]
            return indices

        def eval_line(x0, fx0, x1, fx1, xeval):
            m = (fx1 - fx0)/(x1 - x0)
            return m*xeval - m*x0 + fx0
        
        '''create vector to store the evaluation of the linear splines'''
        yeval = np.zeros_like(xeval)
        
        for jint in range(len(xint) - 1):
            '''find indices of xeval in interval (xint(jint),xint(jint+1))'''
            '''let ind denote the indices in the intervals'''
            '''let n denote the length of ind'''
            ind = find_points(xeval, xint, jint)
            '''temporarily store your info for creating a line in the interval of 
            interest'''
            a1= xint[jint]
            fa1 = yint[jint]
            b1 = xint[jint+1]
            fb1 = yint[jint+1]
            
            for kk in ind:
                '''use your line evaluator to evaluate the lines at each of the points 
                in the interval'''
                '''yeval(ind(kk)) = call your line evaluator at xeval(ind(kk)) with 
                the points (a1,fa1) and (b1,fb1)'''
                yeval[kk] = eval_line(a1, fa1, b1, fb1, xeval[kk])
        
        return yeval

    def natural_cubic_spline(self,xeval=None,xint=None,yint=None):
        # Verify that needed vars are inputted somewhere
        if xeval is None:
            if self.xeval is None:
                raise ValueError("Please input xeval")
            else:
                xeval = self.xeval
        if xint is None:
            if self.xint is None:
                raise ValueError("Please input xint")
            else:
                xint = self.xint
        if yint is None:
            if self.yint is None:
                raise ValueError("Please input yint")
            else:
                yint = self.yint

        def find_points(xeval, xint, idx):
            """
            xeval is the larger array of points
            xint is the smaller array of intervals
            idx is the interval index (counting from 1)
            """
            indices = np.where(np.logical_and(xeval <= xint[idx+1], xeval >= xint[idx]))[0]
            return indices

        def eval_line(x0, fx0, x1, fx1, xeval):
            m = (fx1 - fx0)/(x1 - x0)
            return m*xeval - m*x0 + fx0
        
        Nint = len(xint) - 1

        # Create our linear system AX = B
        h = np.diff(xint)
        A = np.zeros((Nint+1, Nint+1))
        A[0, 0] = 1
        A[-1, -1] = 1
        B = np.zeros((Nint+1, 1))
        for i in range(1, Nint):
            A[i, i] = (h[i - 1] + h[i]) / 3
            A[i, i-1] = h[i - 1] / 6
            A[i, i+1] = h[i] / 6
            B[i, 0] = (yint[i+1] - yint[i])/h[i] - (yint[i] - yint[i-1])/h[i-1]
        X = np.linalg.solve(A, B)

        # TODO: FROM SOLVING THE LINEAR SYS
        
        '''create vector to store the evaluation of the linear splines'''
        yeval = np.zeros_like(xeval)
        
        for jint in range(len(xint) - 1):
            '''find indices of xeval in interval (xint(jint),xint(jint+1))'''
            '''let ind denote the indices in the intervals'''
            '''let n denote the length of ind'''
            ind = find_points(xeval, xint, jint)
            '''temporarily store your info for creating a line in the interval of 
            interest'''
            a1= xint[jint]
            fa1 = yint[jint]
            b1 = xint[jint+1]
            fb1 = yint[jint+1]
            
            for kk in ind:
                '''use your line evaluator to evaluate the lines at each of the points 
                in the interval'''
                '''yeval(ind(kk)) = call your line evaluator at xeval(ind(kk)) with 
                the points (a1,fa1) and (b1,fb1)'''
                yeval[kk] = eval_line(a1, fa1, b1, fb1, xeval[kk])
        
        return yeval




