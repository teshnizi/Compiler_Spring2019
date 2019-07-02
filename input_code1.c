
int arr[5];

int foo (int a, int b, int c){
//    return a + b * 2;
    arr[0] = arr[0] + 1;
    return;
}

void main(void) {
    int x;
    int y;
    int z;
//    x = foo ( x, y, z);
    x = 2 + 5 * 6;
    y = 0;
    z = 3;
    while ( x < 4) {
        if ( y < arr[2] + 7 ){
            foo(x, y, z);
            }
        else {
            foo(y, x, z);
        }
    }
}
