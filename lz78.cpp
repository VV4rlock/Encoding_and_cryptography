#include <string>
#include <map>
#include <vector>
#include <cstring>
#include "stdio.h"
#include <list>
#include <vector>

using namespace std;

int compress(char* input,char* output){
	FILE* in=fopen(input,"rb");
	if (in==NULL){
		printf("Input_file not found\n");
		return -1;
	}
	FILE* out=fopen(output,"wb");
	if (out==NULL)
	{
		printf("Something went wrong(\n");
		fclose(in);
		return -2;
	}
	string buffer="";
	map<string,int> dict;
	char c;
	int dict_len=1;
	int temp;
	while (fread(&c,1,1,in)) {
		if (dict.count(buffer+c)>0)
			buffer+=c;
		else{
			//printf("buf: %s {%d, %d}\n",buffer.c_str(),dict[buffer],c);
			temp=dict[buffer];
			fwrite(&temp,sizeof(int),1,out);
			fwrite(&c,sizeof(char),1,out);
			dict[buffer+c]=dict_len++;
			buffer="";
		}
	}
	printf("Done!\n");
	fclose(in);
	fclose(out);
	return 0;
}

int decompress(char* input,char* output){
	FILE* in=fopen(input,"rb");
	if (in==NULL){
		printf("Input_file not found\n");
		return -1;
	}
	FILE* out=fopen(output,"wb");
	if (out==NULL)
	{
		printf("Something went wrong(\n");
		fclose(in);
		return -2;
	}
	int number,count,word_len;
	char c;
	vector<string> dict;
	vector<int> len_dict;
	dict.push_back("");
	len_dict.push_back(0);
	string word;
	while(!feof(in)){
		count=fread(&number,sizeof(int),1,in);
		if(count==0) break;
		count=fread(&c,sizeof(char),1,in);
		if(count==0) break;
		//printf("{%d, %d}\n",number,c);
		word=dict.at(number)+c;
		word_len=len_dict.at(number)+1;
		//ans+=word;
		fwrite(word.c_str(),word_len,1,out);
		//printf("word: %s |\n", word.c_str());
		dict.push_back(word);
		len_dict.push_back(word_len);
		//if (!DEBUG) printf("<%d,%d,%d>\n",offset,length,(int)c);
		//print_buf();
	}

    printf("Done!\n");



	return 0;
}

int main(int argc, char** argv){	
	if (argc!=4){
		printf("Usage lz78 -c[d] input_file output_file\n");
		return -1;
	}
	int err=0;
	if(!strcmp("-c",argv[1]))
		err=compress(argv[2],argv[3]);
	else if(!strcmp("-d",argv[1]))
		err=decompress(argv[2],argv[3]);
	else{
		printf("Usage lz78 -c[d] input_file output_file\n");
		return -1;
	}
	return err;
}