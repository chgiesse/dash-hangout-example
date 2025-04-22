from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AmazonProduct(Base):
    __tablename__ = 'AmazonProducts'
    __table_args__ = {'schema': 'AnalyticsDM'}
    
    # Primary key
    Id = Column(Integer, primary_key=True)
    
    # Product information
    ProductId = Column(String, index=True, nullable=False)
    ProductName = Column(String)
    Category = Column(String)
    MainCategory = Column(String)
    DiscountedPrice = Column(Integer)
    ActualPrice = Column(Float)
    DiscountPercentage = Column(Float)
    
    # Rating information
    Rating = Column(Float)
    RatingCount = Column(Float)
    RatingSentiment = Column(String)
    
    # Review information
    AboutProduct = Column(String)
    ReviewContent = Column(String)
    ReviewSentiment = Column(String)
    ReviewTitle = Column(String)
    ReviewId = Column(String)
    
    # User information
    UserId = Column(String)
    UserName = Column(String)
    
    # Sales information
    SaleDate = Column(DateTime)
    SaleMonth = Column(String)  # Using String to store Period information
    
    # Image and product links
    ImgLink = Column(String)
    ProductLink = Column(String)
    
    def __repr__(self):
        return f"<AmazonProduct(ProductId='{self.ProductId}', ProductName='{self.ProductName[:20]}...', Rating={self.Rating})>"