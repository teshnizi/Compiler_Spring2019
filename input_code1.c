
void func(int a[], int b[], int c){
    a[1] = 0;
    c = 11;
    return;
}

void main(void){
    int a[2];
    int b[2];
    int c;
    int d;

    c = 10;
    a[1] = 4;
    b[1] = 5;

    func(a, b, c);
}
