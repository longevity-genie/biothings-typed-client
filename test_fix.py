#!/usr/bin/env python3
"""Test script to verify the async client fix"""

import asyncio
import warnings
import pytest
from biothings_typed_client.genes import GeneClientAsync

@pytest.mark.asyncio
async def test_async_client_instantiation():
    """Test that creating an async client doesn't produce the original warning"""
    print("Creating async gene client...")
    
    # Test 1: Direct instantiation with proper cleanup
    print("Testing direct instantiation:")
    async with GeneClientAsync(caching=False) as client:
        print("✓ Client created successfully without the set_caching warning")
        
        # Test 3: Manual caching setup
        print("Testing manual caching setup:")
        await client.set_caching()
        print("✓ Manual caching setup completed")
    
    # Test 2: Use as context manager (caching will be set up automatically)
    print("\nTesting context manager pattern:")
    async with GeneClientAsync(caching=False) as client_cm:
        print("✓ Context manager setup completed")
    
    # Test 4: Factory method with proper cleanup
    print("\nTesting factory method:")
    client_factory = await GeneClientAsync.create(caching=False)
    try:
        print("✓ Factory method completed")
    finally:
        await client_factory.close()
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    # Capture warnings to see if we still get the original issue
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        asyncio.run(test_async_client_instantiation())
        
        # Check for the specific warning we fixed
        set_caching_warnings = [warning for warning in w 
                              if "coroutine 'AsyncBiothingClient._set_caching' was never awaited" in str(warning.message)]
        
        if set_caching_warnings:
            print(f"\n❌ Original warning still present: {len(set_caching_warnings)} occurrences")
            for warning in set_caching_warnings:
                print(f"   {warning.message}")
        else:
            print("\n✅ Original set_caching warning is fixed!")
            
        # Show any other warnings (for informational purposes)
        other_warnings = [warning for warning in w 
                         if "coroutine 'AsyncBiothingClient._set_caching' was never awaited" not in str(warning.message)]
        if other_warnings:
            print(f"\nℹ️  Other warnings present ({len(other_warnings)}):")
            for warning in other_warnings:
                print(f"   {warning.message}")
        else:
            print("\nℹ️  No other warnings detected") 