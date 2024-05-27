await state.update_data(photo = message.photo[-1])
    key, additional_key = await get_hash(message.from_user.id)
    data = await state.get_data()
    file_path = await bot.get_file(data['photo'].file_id)
    photo_binary_data = await bot.download_file(file_path.file_path)
    image = Image.open(photo_binary_data)
    width, height = image.size
    print(f"Ширина: {width} пикселей")
    print(f"Высота: {height} пикселей")
    
    if width < 128 or height < 128:
        await message.answer("Размер фото слишком мал, пришлите другое")
    else:
        path = f"/home/sasha/health_checker/HealthCheck/images/{data['photo'].file_id + str(uuid.uuid4())}.jpg"
        await bot.download(
            data['photo'],
            destination=path
        )
        photo_binary_data = photo_binary_data.read()
        encoded_data = base64.b64encode(photo_binary_data)
        await message.answer("Фото получено. Начат анализ...")
        result = json.loads(rpcClient.call(encoded_data, config.brain_analysis_queue))
        await message.answer(f"Ваш результат: {result}")