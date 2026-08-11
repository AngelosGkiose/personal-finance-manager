import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';


class AuthService {
  static Future<void> register({
    required String username,
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/auth/register'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 201) {
      return;
    }

    final responseBody = jsonDecode(response.body);

    if (responseBody is Map<String, dynamic>) {
      final detail = responseBody['detail'];

      if (detail is String) {
        throw Exception(detail);
      }
    }

    throw Exception('Registration failed');
  }
}