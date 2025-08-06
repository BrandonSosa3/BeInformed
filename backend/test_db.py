from app.db.base import SessionLocal
from app.models.source import Source

# Create a database session
db = SessionLocal()

try:
    # Create a test source
    test_source = Source(
        url="https://example.com/test",
        title="Test Source",
        description="This is a test source",
        source_type="test"
    )
    
    # Add it to the database
    db.add(test_source)
    
    # Commit the transaction
    db.commit()
    
    # Refresh our object with data from the database (to get the ID)
    db.refresh(test_source)
    
    print(f"Created test source with ID: {test_source.id}")
    
    # Query all sources
    sources = db.query(Source).all()
    
    print("\nAll sources in database:")
    for source in sources:
        print(f"  - {source.id}: {source.title} ({source.source_type})")
    
except Exception as e:
    print(f"Error: {e}")
    
    # If anything goes wrong, roll back the transaction
    db.rollback()
    
finally:
    # Always close the database session
    db.close()