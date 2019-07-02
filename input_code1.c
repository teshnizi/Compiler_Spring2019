
void func(int a[], int b){
    a[1] = 4;
    b = 5;
    return;
}


void main(void){
    int a[3];
    int b;
    a[1] = 5;
    b = 7;
    func(a, b);
}
