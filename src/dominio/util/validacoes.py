class Validacao():
	"""Classe destinada a validação geral de valores e ED's"""

	__msg_d_dmax = "O valor de '{}' mín({}) deve ser menor que o máx({})"

	@staticmethod
	def validar_min_max(val_min, val_max, nome_var):
		"""Verifica se mín é menor/igual ao máx e se ambos são não negativos

		Args:
			val_min: Menor valor aceitável
			val_max: Maior valor aceitável
			nome_var: Nome do atributo que será testado (ex: 'velocidade')

		Raises:
			ValueError: Se um dos valores for negativo ou mín maior que máx
		"""

		if val_min < 0 or val_max < 0:
			raise ValueError(f"O valor para {nome_var} deve ser positivo.")

		elif val_min > val_max:
			raise ValueError(
				f"O valor mínimo de {nome_var} deve ser menor que o máximo.")

		return None

	@staticmethod
	def validar_chaves(dic_a: dict, dic_b: dict):
		"""Verifica se ambos dicionários compartilham as mesmas chaves.

		Args:
			dic_a: Primeiro dicionário
			dic_b: Segundo dicionário
			nome_var: Nome do atributo que será testado (ex: 'eixos')

		Raises:
			KeyError: Se ao menos uma chave estiver ausente em um dicionário
		"""
		if {*dic_a} != {*dic_b}:
			raise KeyError(
				"Chave ausente ou com nome distinto em um dos conjuntos.")

		return None

	@staticmethod
	def validar_min_max_dict(dic_val: dict, dic_val_max: dict):
		"""Verifica se cada valor de A respeita o máximo em B (mesma chave).

		Args:
			dic_val: Dicionário com os valores a serem testados
			dic_val_max: Valores máximo permitido para chave de A

		Raises:
			KeyError: Se ao menos uma chave estiver ausente em um dicionário
			ValueError: Se dic_val conter valor maior que dic_val_max
		"""
		Validacao.validar_chaves(dic_val, dic_val_max)

		dv = dic_val
		dvm = dic_val_max

		for k in dic_val:
			if dic_val[k] > dic_val_max[k]:
				raise ValueError(Validacao.__msg_d_dmax.format(k, dv[k], dvm[k]))
