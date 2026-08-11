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


  static Future<String> login({
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/auth/login'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'email': email,
        'password': password,
      }),
    );

    final responseBody = jsonDecode(response.body);

    if (response.statusCode == 200) {
      return responseBody['access_token'];
    }

    if (responseBody is Map<String, dynamic>) {
      final detail = responseBody['detail'];

      if (detail is String) {
        throw Exception(detail);
      }
    }

    throw Exception('Login failed');
  }


  static Future<bool> validateAccessToken(
    String token,
  ) async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/auth/me'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return true;
    }

    if (response.statusCode == 401) {
      return false;
    }

    throw Exception(
      'Could not validate authentication',
    );
  }
}