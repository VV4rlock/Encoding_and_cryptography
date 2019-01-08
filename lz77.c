#include "stdio.h"
#include "string.h"



#define WINDOW_SIZE 2048
#define DEBUG 0

char buf[2*WINDOW_SIZE];
char* buf_f=buf+WINDOW_SIZE;
int end_f_buf=2*WINDOW_SIZE;
int begin_b_buf=WINDOW_SIZE;



void shift_l(int n){
	for(int i=0;i<2*WINDOW_SIZE-n;i++)
		buf[i]=buf[i+n];

	begin_b_buf-=n;
	end_f_buf-=n;
	if (begin_b_buf<0)
		begin_b_buf=0;
}

int switch_buffer(FILE* in,unsigned short int length){
	shift_l(length);
	int count=fread(buf+end_f_buf,1,length,in);
	end_f_buf+=count;
}

void find_matching(unsigned short int* offset,unsigned short int* length){
	int len=0;
	int max_len=0;
	int off=WINDOW_SIZE;
	for(int i=begin_b_buf;i<WINDOW_SIZE;i++)
		if(buf[i]==buf_f[0]){
			len=1;
			while(buf[i+len]==buf_f[len] && i+len<end_f_buf) len++;
			if(len>max_len){
				max_len=len;
				off=i;
			}
		}
	*length=max_len;
	*offset=WINDOW_SIZE-off;	
}

void print_buf(){
	printf("\n");
	for(int i=0;i<2*WINDOW_SIZE;i++){
		if(i==WINDOW_SIZE) printf("|\n");
		printf("%c ",buf[i]<65 || i>end_f_buf?'_':buf[i]);
	}
	printf("|\n");
}

int compress(char* input_file,char* output_file){
	FILE* in=fopen(input_file,"rb");
	if (in==NULL){
		printf("Input_file not found\n");
		return -1;
	}
	FILE* out=fopen(output_file,"wb");
	if (out==NULL)
	{
		printf("Something went wrong(\n");
		fclose(in);
		return -2;
	}
	end_f_buf= fread(buf_f,sizeof(char),WINDOW_SIZE,in);
	end_f_buf+=WINDOW_SIZE;
	unsigned short int length,offset;
	char c;
	while(end_f_buf>WINDOW_SIZE){

		if (DEBUG) print_buf();
		
		length=0,offset=0;
		find_matching(&offset,&length);
		c=length==0?buf_f[0]:buf_f[length];
		switch_buffer(in,length+1);
		if(end_f_buf<=WINDOW_SIZE) c = '\0';

		if(DEBUG) printf("<%d,%d,%c>\n", offset,length,c);

		fwrite(&offset,sizeof(unsigned short int),1,out);
		fwrite(&length,sizeof(unsigned short int),1,out);
		fwrite(&c,sizeof(char),1,out);
	}
	printf("DONE!\n");
	fclose(in);
	fclose(out);
	return 0;
}


int shift_l_dec(int n){
	for(int i=0;i<WINDOW_SIZE;i++)
		buf[i]=buf[i+n];
}


int set_buf(FILE* out,unsigned short int offset, unsigned short int length, char c){
	char temp;
	//printf("WIN %d end %d offset %d\n",WINDOW_SIZE,end_f_buf,offset);
	for(int i=0;i<length;i++,end_f_buf++){
		temp=buf[end_f_buf-offset];
		buf[end_f_buf]=temp;
		if (DEBUG) printf("%c",temp);
		fwrite(&temp,1,1,out);
	}
	buf[end_f_buf++]=c;
	fwrite(&c,1,1,out);
	if (DEBUG) printf("%c",c);
	if(end_f_buf>=WINDOW_SIZE){
		shift_l_dec(end_f_buf-WINDOW_SIZE);
		end_f_buf=WINDOW_SIZE;
	}
	return 0;
}


int decompress(char* input_file,char* output_file){
	FILE* in=fopen(input_file,"rb");
	if (in==NULL){
		printf("Input_file not found\n");
		return -1;
	}
	FILE* out=fopen(output_file,"wb");
	if (out==NULL)
	{
		printf("Something went wrong(\n");
		fclose(in);
		return -2;
	}
	unsigned short int length,offset;
	char c;
	int count;
	end_f_buf=0;
	while(!feof(in)){
		count=fread(&offset,sizeof(unsigned short int),1,in);
		if(count==0) break;
		count=fread(&length,sizeof(unsigned short int),1,in);
		if(count==0) break;
		count=fread(&c,sizeof(char),1,in);
		if(count==0) break;
		//fscanf(in,"%hu%hu%c",&offset,&length,&c);
		//fscanf(temp_buf+2,"%hu",&length);
		//length = (unsigned short int)temp_buf[2]+((unsigned short int)temp_buf[3])*256;
		if (DEBUG) printf("<%d,%d,%d>\n",offset,length,(int)c);
		set_buf(out,offset,length,c);
		
		//print_buf();
	}
	
	printf("DONE!\n");

	fclose(in);
	fclose(out);

	return 0;
}



int main(int argc, char** argv){	
	if (argc!=4){
		printf("Usage lz77 -c[d] input_file output_file\n");
		return -1;
	}
	int err=0;
	if(!strcmp("-c",argv[1]))
		err=compress(argv[2],argv[3]);
	else if(!strcmp("-d",argv[1]))
		err=decompress(argv[2],argv[3]);
	else{
		printf("Usage lz77 -c[d] input_file output_file\n");
		return -1;
	}
	return err;
}