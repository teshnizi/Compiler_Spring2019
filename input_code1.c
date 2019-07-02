int b[2];

void func(int a[]){

    a[3] = 4;
}


void main(void){
    int b;
    int c;
    int a[4];
    a[1] = 2;
    func(a);
}
