
int arr[5];

int foo (int a, int b, int c){
//    return a + b * 2;
    arr[0] = 1;
    return a + b;
}

void main(void) {
    int x;
    int y;
    int z;
    x = 2 + 5 * 6;
    y = 0;
    z = 3;
    while ( x < 4) {
        if ( y < arr[2] + 7 ){
            x = foo(x, y, z);
            }
        else {
            y = foo(y, x, z);
        }
    }
}
