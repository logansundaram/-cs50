#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            int avg =
                round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            // Update pixel values
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
}

int cap(int val)
{
    if (val > 255)
    {
        return 255;
    }
    else
    {
        return val;
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            int sepiaRed = cap(round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen +
                                     .189 * image[i][j].rgbtBlue));
            int sepiaGreen = cap(round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen +
                                       .168 * image[i][j].rgbtBlue));
            int sepiaBlue = cap(round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen +
                                      .131 * image[i][j].rgbtBlue));

            // Update pixel with sepia values
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swap pixels
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            float counter = 0.00;
            int totalr = 0;
            int totalb = 0;
            int totalg = 0;
            for (int a = i - 1; a < i + 2; a++)
            {
                for (int b = j - 1; b < j + 2; b++)
                {
                    if ((a >= 0 && a < height) && (b >= 0 && b < width))
                    {
                        totalr += copy[a][b].rgbtRed;
                        totalg += copy[a][b].rgbtGreen;
                        totalb += copy[a][b].rgbtBlue;
                        counter++;
                    }
                }
            }
            RGBTRIPLE avg;
            avg.rgbtRed = round(totalr / counter);
            avg.rgbtGreen = round(totalg / counter);
            avg.rgbtBlue = round(totalb / counter);
            image[i][j] = avg;
        }
    }
}
