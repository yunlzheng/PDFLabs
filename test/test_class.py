class TestClass():  
    arr1 = 2  
    arr2 = 2  
      
    def setUp(self):  
        self.arr1 = 2  
        self.arr2 = 2  
        print "MyTestClass setup"  
  
    def tearDown(self):  
        print "MyTestClass teardown"  
          
    def Testfunc1(self):  
        assert self.arr1 == self.arr2  
      
    def Testfunc2(self):  
        assert self.arr1 == 2  