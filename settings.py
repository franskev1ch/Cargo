
with open('C:/Users/Asus/source/repos/practice/practice.py', 'r+', encoding='utf-8') as f:
	file = f.readlines()
	for i in range(len(file)):
		line = file[i]
		if 'source_path' in line:
			print('Текущая директория исходников:')
			print(line)
			print('Введите новую если хотите изменить, ничего не вводите, если хотите оставить')
			new_source_path = input()
			if new_source_path != '':
				new_source_path = 'source_path="' + new_source_path + '"\n'
				file[i] = new_source_path
		if 'result_path' in line:
			print('Текущая директория результатов:')
			print(line)
			print('Введите новую если хотите изменить, ничего не вводите, если хотите оставить')
			new_result_path = input()
			if new_result_path != '':
				new_result_path = 'result_path="' + new_result_path + '"\n'
				file[i] = new_result_path
	f.seek(0)
	f.writelines(file)

