"""
AURELION Memory-Lite Quick Start Example
"""

from aurelion_memory_lite import Architecture

def main():
    # Initialize architecture
    arch = Architecture()
    
    print("AURELION Memory-Lite: 5-Floor Knowledge Architecture")
    print("=" * 50)
    
    for floor_num, floor_name in arch.get_all_floors().items():
        print(f"Floor {floor_num}: {floor_name}")
    
    print("\nReady to organize your knowledge!")

if __name__ == "__main__":
    main()
